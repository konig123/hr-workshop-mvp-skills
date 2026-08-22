#!/usr/bin/env python3
"""Pulse survey artefacts (reportlab PDF + matplotlib PNG) per pulse_survey.md."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import matplotlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
from matplotlib import patches as mpatches

from reportlab.lib import colors as RL
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

SCALE = "1–5 Likert"

# Runtime config (set in main via CLI)
BASE: Path
CSV: Path
OUT_DIR: Path
INDIV: Path
TEAM_NAME: str
PERIOD: str


@dataclass
class Bands:
    leader: list[str]
    dept_head: list[str]
    team: list[str]
    engagement: list[str]


def band_columns(df: pd.DataFrame) -> Bands:
    qcols = [c for c in df.columns if c.startswith("Q") and "_" in c]
    by_n = {}
    for c in qcols:
        n = int(c.split("_")[0].replace("Q", ""))
        by_n.setdefault(n, c)
    ordered = [by_n[n] for n in sorted(by_n.keys())]
    return Bands(
        leader=ordered[0:10],
        dept_head=ordered[10:13],
        team=ordered[13:17],
        engagement=ordered[17:20],
    )


PALETTE_NAVY = RL.HexColor("#1F3864")
PALETTE_BLUE = RL.HexColor("#2F5496")
PALETTE_ACC = RL.HexColor("#4472C4")
PALETTE_ROW = RL.HexColor("#F2F7FF")
PALETTE_GRID = RL.HexColor("#D9E2F3")
PALETTE_DNG = RL.HexColor("#C00000")
PALETTE_NOTE = RL.HexColor("#EBF3FB")

DIM_LABELS = [
    "Leader Q1",
    "Leader Q2",
    "Leader Q3",
    "Leader Q4",
    "Leader Q5",
    "Leader Q6",
    "Leader Q7",
    "Leader Q8",
    "Leader Q9",
    "Leader Q10",
    "Dept Head Q11 Vision",
    "Dept Head Q12 Strategy",
    "Dept Head Q13 Accessibility",
    "Team Goal Clarity",
    "Team Collaboration",
    "Team Resources",
    "Team Efficiency",
    "Engagement Pride",
    "Engagement Stay Intent",
    "Engagement Referral",
]


def _gap_note(direct: float, overall: float, gmeans: dict[str, float]) -> str:
    gap = direct - overall  # positive when direct pillar stronger than blended experience
    if abs(gap) < 0.05:
        return "Minimal gap — blended experience aligned with direct-leader pillar."
    if gap >= 0.15:
        drag = sorted(gmeans.items(), key=lambda kv: kv[1])[0][0]
        return f"Pillar-vs-overall delta {gap:.2f}: shared scores (notably '{drag}') pull overall below direct-manager signal."
    if gap <= -0.15:
        return (
            "Pillar-vs-overall delta negative: dept / teaming / engagement averages exceed direct-manager scores — contextual lift."
        )
    return "Moderate divergence between pillar and blended scores — review shared dimensions."

def analyse() -> dict:
    df0 = pd.read_csv(CSV, encoding="utf-8-sig").dropna(how="all").copy()
    b = band_columns(df0)
    all_cols = b.leader + b.dept_head + b.team + b.engagement
    vals = df0[all_cols].astype(float)

    dl = vals[b.leader].mean(axis=1)
    ov = vals.mean(axis=1)
    dfa = df0.assign(_dl=dl.values, _overall=ov.values)
    grp = dfa.groupby("Manager", sort=False)

    leaders = sorted(dfa["Manager"].unique(), key=lambda m: grp.get_group(m)["_dl"].mean(), reverse=True)

    rankings = []
    q_means = {}
    workloads = vals[[b.team[2], b.team[3]]].mean(axis=1)  # resources + efficiency
    mood = vals[b.engagement].mean(axis=1)
    atmos = vals[[b.team[0], b.team[1]]].mean(axis=1)  # goal clarity + collaboration
    mgr = dfa["Manager"]
    wl_leader = workloads.groupby(mgr).mean().reindex(leaders)
    md_leader = mood.groupby(mgr).mean().reindex(leaders)
    at_leader = atmos.groupby(mgr).mean().reindex(leaders)

    composite_pressure = pd.DataFrame({"w": wl_leader, "m": md_leader, "a": at_leader}).mean(axis=1)

    def alert_label(x: float) -> str:
        if x < 4.15:
            return "Danger"
        if x < 4.50:
            return "Caution"
        if x < 4.65:
            return "Watch"
        if x <= 4.75:
            return "Normal"
        return "Optimal"

    extremes = []

    bu_q = vals.mean(axis=0)
    for m in leaders:
        gidx = grp.get_group(m).index
        gv = vals.loc[gidx]

        rankings.append(
            {
                "manager": m,
                "n": int(len(gidx)),
                "direct": float(gv[b.leader].mean().mean()),
                "overall": float(gv.mean().mean()),
            }
        )
        qmeans = gv.mean(axis=0)
        q_means[m] = qmeans
        extreme_dims = []
        for col in all_cols:
            low = int((gv[col] <= 2).sum())
            if low:
                extreme_dims.append(f"{col.split('_')[0]}×{low}")
        if extreme_dims:
            extremes.append({"manager": m, "n": len(gidx), "dims": ", ".join(sorted(extreme_dims)[:12]), "count_low": sum(1 for c in gv.to_numpy().flatten() if c <= 2)})

    dim_compare = pd.DataFrame(
        {
            m: pd.Series(
                {
                    "Direct Leader": float(q_means[m][b.leader].mean()),
                    "Dept head": float(q_means[m][b.dept_head].mean()),
                    "Team support": float(q_means[m][b.team].mean()),
                    "Engagement": float(q_means[m][b.engagement].mean()),
                }
            )
            for m in leaders
        }
    ).T.sort_values("Direct Leader", ascending=False)

    shared_teamwide = pd.Series({
        "Dept head (BU)": vals[b.dept_head].mean().mean(),
        "Team support": vals[b.team].mean().mean(),
        "Engagement": vals[b.engagement].mean().mean(),
    })

    variance_row = []
    low_rate_row = []
    for m in leaders:
        gidx = grp.get_group(m).index
        gv = vals.loc[gidx]
        v_per_q = gv.var(ddof=0)
        variance_row.append(float(v_per_q.mean()))
        pct_low = float((gv.to_numpy() <= 2).mean() * 100)
        low_rate_row.append(pct_low)

    return {
        "df": dfa,
        "bands": b,
        "all_cols": all_cols,
        "vals": vals,
        "grp": grp,
        "leaders": leaders,
        "rankings": rankings,
        "q_means": q_means,
        "gap_notes": {
            rankings[i]["manager"]: _gap_note(rankings[i]["direct"], rankings[i]["overall"], {
                "Dept trio": grp.get_group(rankings[i]["manager"])[b.dept_head].astype(float).mean().mean(),
                "Team block": grp.get_group(rankings[i]["manager"])[b.team].astype(float).mean().mean(),
                "Engagement trio": grp.get_group(rankings[i]["manager"])[b.engagement].astype(float).mean().mean(),
            })
            for i in range(len(rankings))
        },
        "dim_compare": dim_compare,
        "shared_teamwide": shared_teamwide,
        "bu_q": bu_q,
        "bu_dl": float(dl.mean()),
        "bu_ov": float(ov.mean()),
        "pressure_tbl": pd.DataFrame(
            {
                "Workload (res+eff)": wl_leader,
                "Mood (engagement)": md_leader,
                "Team atmosphere (goals+collab)": at_leader,
                "Pressure composite": composite_pressure,
                "Alert": composite_pressure.apply(alert_label),
            }
        ),
        "variances": dict(zip(leaders, variance_row, strict=False)),
        "low_rates": dict(zip(leaders, low_rate_row, strict=False)),
        "extremes_tbl": extremes,
        "pressure_shared_lt_415": bool(shared_teamwide["Team support"] < 4.15),
    }


def _margins(cm=2.2):
    return cm * 10  # pt approx from mm via reportlab: 22mm margins


def fmt_table(data, colw=None):
    tbl = Table(data, colWidths=colw)
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PALETTE_ACC),
                ("TEXTCOLOR", (0, 0), (-1, 0), RL.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, PALETTE_GRID),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [RL.white, PALETTE_ROW]),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )
    return tbl


def _styles():
    bs = getSampleStyleSheet()
    body = ParagraphStyle(
        name="Body",
        parent=bs["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        textColor=PALETTE_NAVY,
    )
    justified = ParagraphStyle(
        name="Just",
        parent=bs["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
    )
    h1 = ParagraphStyle(name="H1", parent=bs["Title"], alignment=TA_CENTER, textColor=PALETTE_NAVY, fontSize=16, spaceAfter=8)
    h2 = ParagraphStyle(name="H2", parent=bs["Heading2"], textColor=PALETTE_NAVY)
    quote = ParagraphStyle(name="Quote", parent=justified, leftIndent=6, borderPadding=8, borderColor=PALETTE_ACC)
    return body, justified, h1, h2, quote


def build_team_pdf(ctx: dict) -> Path:
    body, just, h1, h2, quote = _styles()
    outp = OUT_DIR / f"{TEAM_NAME} Pulse Survey Report - {PERIOD}.pdf"
    doc = SimpleDocTemplate(
        str(outp),
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=26 * mm,
        bottomMargin=20 * mm,
    )

    preamble = """<b>Two averages matter.</b> <b>Direct Leader score</b> averages Q1–Q10 only.
    <b>Overall average</b> blends twenty items (dept leadership, teaming, engagement). Interpret Leader impact via pillar means;
    blended averages describe holistic context. Rating scale assumption: %s.<br/><br/>
    Structural map: Leader Q1–Q10 · Dept Head Q11–Q13 · Team Q14–Q17 · Engagement Q18–Q20.
    Invitation roster was not supplied — response-rate cells show only completed n. No verbatim open-text column present in supplied extract.
    """

    story: list = [Paragraph("<b>Pulse Survey Team Report — %s (%s)</b>" % (TEAM_NAME, PERIOD), h1)]
    story.append(Paragraph(preamble.replace("\n", " ") % SCALE, just))

    summary_f = (
        f"This pulse captured <b>{len(ctx['df'])}</b> completions. Company pillar mean "
        f"<b>{ctx['bu_dl']:.3f}</b> vs blended <b>{ctx['bu_ov']:.3f}</b>. "
        f"Top pillar scorer: <b>{ctx['rankings'][0]['manager']}</b> "
        f"({ctx['rankings'][0]['direct']:.3f}). Variance and ≤2 tails matter more than middling averages where sample sizes permit.<br/><br/>"
        "<b>Operating priorities:</b>"
        "<br/>• Elevate teaming/resources/process signals when composite pressure dips."
        "<br/>• Pair HRBP follow-ups wherever pillar-vs-blended gaps exceed tolerance."
        "<br/>• Diffuse managerial practices from the highest-performing pillar scorer."
        "<br/>• Keep accessibility on BU leadership agendas when Q13 softness repeats."
        "<br/>• Maintain transparency that Q14–Q17 are systemic, not attributable to individuals."
    )
    story.append(Paragraph(summary_f, just))
    story.append(Spacer(1, 8))

    tab = [["Rank", "Leader", "n", "Response note", "Direct Leader", "Overall", "Gap notes"]]
    for i, r in enumerate(ctx["rankings"], 1):
        tab.append(
            [
                str(i),
                str(r["manager"]),
                str(r["n"]),
                "Invite base missing — n=completes",
                f"{r['direct']:.3f}",
                f"{r['overall']:.3f}",
                ctx["gap_notes"][r["manager"]],
            ]
        )
    story.append(Paragraph("<b>I. Overall Rankings</b>", h2))
    story.append(fmt_table(tab, None))
    story.append(PageBreak())

    cmp_rows = [["Leader", "Direct Leader", "Dept head", "Team support", "Engagement"]]
    dc = ctx["dim_compare"].loc[ctx["leaders"]]
    for m in ctx["leaders"]:
        cmp_rows.append(
            [
                m,
                f"{dc.loc[m, 'Direct Leader']:.3f}",
                f"{dc.loc[m, 'Dept head']:.3f}",
                f"{dc.loc[m, 'Team support']:.3f}",
                f"{dc.loc[m, 'Engagement']:.3f}",
            ]
        )
    cmp_rows.append(
        [
            "BU mean",
            f"{ctx['vals'][ctx['bands'].leader].mean().mean():.3f}",
            f"{ctx['vals'][ctx['bands'].dept_head].mean().mean():.3f}",
            f"{ctx['vals'][ctx['bands'].team].mean().mean():.3f}",
            f"{ctx['vals'][ctx['bands'].engagement].mean().mean():.3f}",
        ]
    )
    story.append(Paragraph("<b>II. Cross-leader dimension comparison</b>", h2))
    story.append(
        Paragraph(
            "Highest / lowest pillars per Leader are surfaced in charts; BU-wide team-support composite "
            + ("is &lt;4.15 (danger-zone proxy) — treat as systemic." if ctx["pressure_shared_lt_415"] else "clears typical danger threshold but still warrants monitoring."),
            just,
        )
    )
    story.append(fmt_table(cmp_rows, None))

    story.append(PageBreak())
    story.append(Paragraph("<b>III. Deep dives — Individuals</b>", h2))

    def leader_blurb(manager: str) -> str:
        g = ctx["grp"].get_group(manager)
        n = len(g)
        b = ctx["bands"]
        lmeans = g[b.leader].astype(float).mean()
        lows = list(lmeans.nsmallest(3).index)
        highs = list(lmeans.nlargest(3).index)

        samp = "(directional guidance only — sample ≤10)" if n <= 10 else ""
        interp = ""
        pillar = ctx["q_means"][manager][b.leader].mean()
        team_avg = ctx["q_means"][manager][b.team].mean()

        if team_avg + 0.05 < pillar:
            interp += (
                " Signals suggest teaming/resourcing/process drag beyond direct-manager ownership; escalate with BU operator + HRBP."
            )

        lows_txt = "; ".join(
            f"{DIM_LABELS[b.leader.index(q)]} ({float(lmeans[q]):.2f})" for q in lows
        )
        highs_txt = "; ".join(f"{DIM_LABELS[b.leader.index(q)]} ({float(lmeans[q]):.2f})" for q in highs)

        return (
            f"<b>{manager}</b> | Direct pillar <b>{ctx['rankings'][ctx['leaders'].index(manager)]['direct']:.2f}</b> | Overall <b>"
            f"{ctx['rankings'][ctx['leaders'].index(manager)]['overall']:.2f}</b> | <i>n={n}</i><br/><br/>"
            f"<u>Strengths</u>: {highs_txt}.<br/>"
            f"<u>Issues</u>: scrutinise {lows_txt}; pair with numeric deep dive on ≤2 responses.<br/>"
            f"<u>Interpretation</u>: {interp or 'Signals relatively balanced versus peers; reinforce steady-state habits.'}<br/><br/><i>{samp}</i><br/><br/>"
        )

    for m in ctx["leaders"]:
        story.append(Paragraph(leader_blurb(m), just))

    story.append(PageBreak())
    story.append(Paragraph("<b>IV. Work pressure composites</b>", h2))
    pdf_press = [["Leader", "Workload", "Mood/state", "Team atmosphere", "Composite", "Alert"]]
    for m in ctx["leaders"]:
        row = ctx["pressure_tbl"].loc[m]
        pdf_press.append(
            [
                m,
                f"{row['Workload (res+eff)']:.3f}",
                f"{row['Mood (engagement)']:.3f}",
                f"{row['Team atmosphere (goals+collab)']:.3f}",
                f"{row['Pressure composite']:.3f}",
                row["Alert"],
            ]
        )
    story.append(fmt_table(pdf_press, None))
    story.append(
        Paragraph(
            "Composite blends resource/efficiency (workload proxy), engagement (mood), and teaming climate (goal clarity + collaboration)."
            " Read low composites as systemic — owners sit with department operators and portfolio leadership rather than blaming individual managers.",
            just,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("<b>V. Senior leadership overall</b>", h2))
    bu13 = ctx["vals"][ctx["bands"].dept_head].mean()
    dept_tbl = [["Question", "Company mean"]] + [[q.split("_")[0], f"{float(bu13[q]):.3f}"] for q in ctx["bands"].dept_head]
    story.append(fmt_table(dept_tbl, None))
    worst_m = dc["Dept head"].idxmin()
    best_m = dc["Dept head"].idxmax()
    story.append(
        Paragraph(
            f"Softest departmental ratings cluster under <b>{worst_m}</b> versus strongest under <b>{best_m}</b>; "
            "discuss causal factors (strategy clarity vs accessibility logistics) offline before attributing variance to Managers.",
            just,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("<b>VI. Infrastructure & teaming</b>", h2))
    bu_team = ctx["vals"][ctx["bands"].team].mean()
    team_tbl = [["Question", "Company mean"]] + [[q.split("_")[0], f"{float(bu_team[q]):.3f}"] for q in ctx["bands"].team]
    story.append(fmt_table(team_tbl, None))
    story.append(Paragraph("<i>Interpret as systemic teaming/process variables — avoid naming individual Leaders.</i>", just))

    story.append(PageBreak())
    story.append(Paragraph("<b>VII. Open-text feedback</b>", h2))
    story.append(
        Paragraph(
            "Structured comments were unavailable in supplied raw data. Silence may reflect survey fatigue "
            "or anonymity trust issues — HR should consider supplementary qualitative pulses if themes are required.",
            just,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("<b>VIII. Action tiers</b>", h2))
    act = [
        ["Priority", "Action", "Owner"],
        ["P0", "Address systemic teaming/resource strain + accessibility themes across BU", "Department head portfolio"],
        ["P1", "Target HRBP/coaching checkpoints for divergence + pressure alerts", "HR / BU chief of staff"],
        ["P2", "Codify behavioural recipes from pillar leaders via peer demos", "HR / community of practice"],
    ]
    story.append(fmt_table(act, None))

    def on_page(canv: Canvas, doc):
        canv.saveState()
        canv.setStrokeColor(PALETTE_NAVY)
        canv.line(22 * mm, A4[1] - 18 * mm, A4[0] - 22 * mm, A4[1] - 18 * mm)
        canv.setFont("Helvetica", 9)
        canv.setFillColor(PALETTE_NAVY)
        canv.drawCentredString(A4[0] / 2, 10 * mm, f"{TEAM_NAME} Pulse · {PERIOD}")
        canv.drawRightString(A4[0] - 22 * mm, A4[1] - 24 * mm, f"page {doc.page}")
        canv.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return outp


def build_composite_png(ctx: dict) -> Path:
    matplotlib.rcParams.update(
        {
            "font.family": ["Arial Unicode MS", "Heiti TC", "DejaVu Sans", "sans-serif"],
            "axes.unicode_minus": False,
        }
    )
    leaders = ctx["leaders"]
    lbl = [m.replace("Mgr.", "").strip() for m in leaders]
    b = ctx["bands"]
    vals = ctx["vals"]

    pillar_means = [float(ctx["q_means"][m][b.leader].mean()) for m in leaders]
    pillar_std = [float(ctx["grp"].get_group(m)["_dl"].std(ddof=0)) for m in leaders]
    bu_mu = float(vals[b.leader].mean().mean())

    heat = np.vstack([ctx["q_means"][m][ctx["all_cols"]].astype(float).to_numpy() for m in leaders]).T

    fig = plt.figure(facecolor="#f8f9fa", figsize=(20, 28))
    gs = gridspec.GridSpec(4, 2, figure=fig, height_ratios=[1.0, 1.0, 1.0, 0.7])
    x = np.arange(len(leaders))

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor("#ffffff")
    ax1.bar(x, pillar_means, yerr=pillar_std, capsize=5, color="#4472C4", ecolor="#1F3864")
    ax1.axhline(bu_mu, color="#C00000", linestyle="--", lw=2, label="Company pillar avg")
    for i, pm in enumerate(pillar_means):
        n_here = int(ctx["grp"].get_group(leaders[i]).shape[0])
        ax1.text(
            i,
            pm + pillar_std[i] + 0.05,
            f"{pm:.2f}\n(n={n_here})",
            ha="center",
            fontsize=9,
            color="#1F3864",
        )
    ax1.set_xticks(x)
    ax1.set_xticklabels(lbl, rotation=35, ha="right")
    ax1.set_ylim(3, 5.05)
    ax1.set_ylabel("Mean")
    ax1.set_title("Leader rankings (pillar + respondent SD)")
    ax1.legend(fontsize=8)
    ax1.grid(axis="y", alpha=0.35)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor("#ffffff")
    im = ax2.imshow(heat, cmap="RdYlGn", aspect="auto", vmin=3, vmax=5)
    qlabels = [c.replace("_", " ")[:26] for c in ctx["all_cols"]]
    ax2.set_yticks(range(len(ctx["all_cols"])))
    ax2.set_yticklabels(qlabels, fontsize=7)
    ax2.set_xticks(range(len(leaders)))
    ax2.set_xticklabels(lbl, rotation=35, ha="right")
    for i in range(heat.shape[0]):
        for j in range(heat.shape[1]):
            ax2.text(j, i, f"{heat[i, j]:.1f}", ha="center", va="center", fontsize=8, color="black")
    ax2.set_title("Dimension heatmap (rows = survey items)")
    plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)

    stacks = []
    for m in leaders:
        idx = ctx["grp"].get_group(m).index
        gvals = vals.loc[idx].to_numpy().ravel()
        stacks.append([(gvals == s).mean() * 100 for s in range(1, 6)])
    stacks = np.asarray(stacks).T

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor("#ffffff")
    bottoms = np.zeros(len(leaders))
    cmap_st = ["#C00000", "#FF9933", "#FFF176", "#AEEA94", "#1B7F3A"]
    rating_labels = []
    for r in range(5):
        vals_row = stacks[r]
        ax3.bar(x, vals_row, bottom=bottoms, color=cmap_st[r], edgecolor="white", linewidth=0.35)
        rating_labels.append(mpatches.Patch(color=cmap_st[r], label=f"{r+1}s"))
        bottoms = bottoms + vals_row
    ax3.set_xticks(x)
    ax3.set_xticklabels(lbl, rotation=35, ha="right")
    ax3.set_ylabel("% responses")
    ax3.set_title("Score distribution (% 1–5, all Likert)")
    ax3.legend(handles=rating_labels, ncol=5, fontsize=8, loc="upper right")

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor("#ffffff")
    vx = np.array([ctx["variances"][m] for m in leaders])
    ax4.bar(x, vx, color="#4472C4")
    ax4.set_xticks(x)
    ax4.set_xticklabels(lbl, rotation=35, ha="right")
    ax4.set_ylabel("Avg item variance")

    lr_ax = ax4.twinx()
    lr_ax.plot(x, [ctx["low_rates"][m] for m in leaders], color="#C00000", marker="o", linestyle="--", linewidth=2)
    lr_ax.set_ylabel("% ratings ≤ 2")
    lr_ax.tick_params(colors="#C00000")
    ax4.set_title("Variance & low-score rate")

    ax5 = fig.add_subplot(gs[2, 0])
    ax5.set_facecolor("#ffffff")
    wl = np.array([float(ctx["pressure_tbl"].loc[m, "Workload (res+eff)"]) for m in leaders])
    colwl = []
    for score in wl:
        colwl.append("#C00000" if score < 4.0 else "#FFA500" if score <= 4.4 else "#228B22")
    ax5.barh(lbl, wl, color=colwl)
    ax5.axvline(4.0, color="#555555", linestyle="--")
    ax5.axvline(4.4, color="#555555", linestyle="--")
    ax5.set_title("Workload proxy")
    ax5.set_xlim(2.85, 5.05)

    ax6 = fig.add_subplot(gs[2, 1])
    ax6.set_facecolor("#ffffff")
    nm = []
    vv = []
    for k, v in ctx["shared_teamwide"].items():
        nm.append(str(k))
        vv.append(float(v))
    cols = ["#C00000" if v < 4.15 else "#FFA500" if v < 4.5 else "#4472C4" for v in vv]
    ax6.barh(nm, vv, color=cols)
    ax6.axvline(4.15, linestyle="--", color="#000000")
    ax6.set_xlim(3.4, 5.05)
    ax6.set_title("Company shared-dimension averages")

    ax7 = fig.add_subplot(gs[3, :])
    ax7.axis("off")
    xt_rows_header = [["Leader", "n", "Example ≤2 hotspots", "Total ≤2"]]
    if ctx["extremes_tbl"]:
        body_rows = [[r["manager"], str(r["n"]), r["dims"], str(r["count_low"])] for r in ctx["extremes_tbl"]]
    else:
        body_rows = [["", "", "No hotspots detected", "0"]]
    tbl = ax7.table(
        cellText=body_rows,
        colLabels=xt_rows_header[0],
        cellLoc="left",
        loc="upper center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)

    outp = OUT_DIR / f"{TEAM_NAME} Pulse Survey Charts - {PERIOD}.png"
    plt.tight_layout()
    fig.savefig(outp, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return outp


def label_support(score: float, bu_avg: float) -> str:
    if score < 3.6 or score < bu_avg - 0.35:
        return "[Critical]"
    if score + 0.05 < bu_avg:
        return "[Watch]"
    if score < bu_avg - 0.1:
        return "[Below BU avg]"
    return "[Good]"


def build_personal_pdf(ctx: dict, manager: str) -> Path:
    _, just, _, h2, __ = _styles()
    outp = (INDIV / f"{manager} - Pulse Survey Personal Report.pdf").resolve()
    doc = SimpleDocTemplate(
        str(outp),
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=26 * mm,
        bottomMargin=20 * mm,
    )
    gdf = ctx["grp"].get_group(manager)
    b = ctx["bands"]
    bu = ctx["bu_q"]
    gv = ctx["vals"].loc[gdf.index]

    pill = float(ctx["q_means"][manager][b.leader].mean())
    overall = float(gv.mean().mean())
    dept = float(gv[b.dept_head].mean().mean())
    team_mu = float(gv[b.team].mean().mean())
    eng_mu = float(gv[b.engagement].mean().mean())
    std_internal = float(gdf["_dl"].std(ddof=0))
    min_ov = float(gdf["_overall"].min())
    max_ov = float(gdf["_overall"].max())

    bu_pill = float(bu[b.leader].mean())
    bu_dept = float(bu[b.dept_head].mean())
    bu_team = float(bu[b.team].mean())
    bu_eng = float(bu[b.engagement].mean())

    def row(label: str, you: float, baseline: float, dash: bool = False):
        if dash:
            return [label, f"{you:.3f}", "—", "—"]
        d = you - baseline
        sgn = "+" if d >= 0 else ""
        return [label, f"{you:.3f}", f"{baseline:.3f}", f"{sgn}{d:.3f}"]

    story = []
    hdr = ParagraphStyle(
        "ph",
        parent=just,
        alignment=TA_CENTER,
        fontSize=14,
        textColor=PALETTE_NAVY,
        spaceAfter=10,
    )
    story.append(Paragraph("<b>%s</b><br/><i>n=%s · %s · Personal digest</i>" % (manager, len(gdf), PERIOD), hdr))

    t1 = [["Metric", "You", "Company", "Delta"]]
    t1.extend(
        [
            row("Overall blend", overall, ctx["bu_ov"]),
            row("Direct pillar", pill, bu_pill),
            row("Dept-head trio", dept, bu_dept),
            row("Team support trio", team_mu, bu_team),
            row("Engagement trio", eng_mu, bu_eng),
        ]
    )
    t1.append(row("StdDev (pillar dispersion)", std_internal, 0.0, dash=True))
    t1[-1][2], t1[-1][3] = "—", "—"
    t1.append(["Min/Max respondent blend", f"{min_ov:.2f} / {max_ov:.2f}", "—", "—"])

    story.append(Paragraph("<b>I. Score overview</b>", h2))
    story.append(fmt_table(t1, None))

    pillar_order = ctx["q_means"][manager][b.leader].sort_values(ascending=False)
    hi = [["Item", "You", "BU", "Delta"]]
    for q, sc in pillar_order.head(3).items():
        hi.append(
            [DIM_LABELS[b.leader.index(q)][:40], f"{float(sc):.3f}", f"{float(bu[q]):.3f}", f"{float(sc - bu[q]):+.3f}"]
        )
    story.append(Paragraph("<b>II. Pillar highs</b>", h2))
    story.append(fmt_table(hi, None))

    lo = [["Item", "You", "BU", "Delta"]]
    for q, sc in pillar_order.tail(3).items():
        lo.append(
            [DIM_LABELS[b.leader.index(q)][:40], f"{float(sc):.3f}", f"{float(bu[q]):.3f}", f"{float(sc - bu[q]):+.3f}"]
        )
    story.append(Paragraph("<b>III. Watch-list items</b>", h2))
    story.append(fmt_table(lo, None))

    t_te = [["Question", "You", "BU", "Label"]]
    for q in b.team:
        sc = float(gv[q].mean())
        t_te.append([q.split("_")[0], f"{sc:.3f}", f"{float(bu[q]):.3f}", label_support(sc, float(bu[q]))])
    story.append(Paragraph("<b>IV. Team support (systemic)</b>", h2))
    story.append(fmt_table(t_te, None))
    story.append(Paragraph("<i>*These cues describe teaming context—not the Leader alone.*</i>", just))

    t_de = [["Item", "You", "BU", "Delta"]]
    for q in b.dept_head + b.engagement:
        sc = float(gv[q].mean())
        t_de.append(
            [DIM_LABELS[ctx["all_cols"].index(q)][:40], f"{sc:.3f}", f"{float(bu[q]):.3f}", f"{sc - float(bu[q]):+.3f}"]
        )
    story.append(Paragraph("<b>V. Dept head / engagement specifics</b>", h2))
    story.append(fmt_table(t_de, None))

    story.append(PageBreak())
    story.append(Paragraph("<b>VI. Commentary</b>", h2))
    story.append(
        Paragraph(
            "No raw-text comments travelled with CSV—deploy focused listening loops if anecdotes are absent.",
            just,
        )
    )

    tips = []
    if pill > 4.8:
        tips.append("Lead with affirmation, explore stretch charters, capture sponsorship commitments.")
    elif pill >= 4.5:
        tips.append("Pressure-test weakest pillar probes with behavioural examples from your team.")
    else:
        tips.append("Treat every ≤2 as a forensic signal—meet with HRBP before mandating behavioural fixes.")

    if team_mu < bu_team - 0.07:
        tips.append("Name resource/teaming hurdles transparently—even when outcomes depend on other functions.")

    story.append(Paragraph("<b>VII. 1:1 themes</b>", h2))
    story.append(Paragraph("<br/>".join("• " + t for t in tips), just))

    def on_pg(canv: Canvas, doc):
        canv.saveState()
        canv.setFont("Helvetica", 8)
        canv.setFillColor(PALETTE_NAVY)
        canv.drawCentredString(A4[0] / 2, 10 * mm, f"{manager} · personal pulse · {PERIOD}")
        canv.restoreState()

    doc.build(story, onFirstPage=on_pg, onLaterPages=on_pg)
    return outp


def build_personal_png(ctx: dict, manager: str) -> Path:
    matplotlib.rcParams.update(
        {"font.family": ["Arial Unicode MS", "DejaVu Sans", "sans-serif"], "axes.unicode_minus": False}
    )
    b = ctx["bands"]
    rows = ctx["vals"].loc[ctx["grp"].get_group(manager).index]

    grp_mean_l = rows[b.leader].mean()
    bu_l = ctx["bu_q"][b.leader].astype(float)
    yidx = np.arange(len(b.leader))
    widths = [float(grp_mean_l[q]) for q in b.leader]
    colours = []
    for q in b.leader:
        sc = float(grp_mean_l[q])
        colours.append("#C00000" if sc + 1e-9 < float(bu_l[q]) else "#4472C4")

    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1.55, 1])
    gs_r = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1])

    ax_a = fig.add_subplot(gs[0])
    ax_a.barh(yidx, widths, color=colours, height=0.55)
    ax_a.axvline(float(bu_l.mean()), linestyle="--", color="#333333")
    for yi, w, q in zip(yidx, widths, b.leader, strict=False):
        bub = float(bu_l[q])
        ax_a.text(w + 0.05, yi, "%.2f (%+.2f)" % (w, w - bub), va="center", fontsize=9)
    ax_a.set_yticks(yidx)
    ax_a.set_yticklabels([q.split("_")[0] for q in b.leader])
    ax_a.set_title("%s pillar vs BU" % manager.replace("Mgr.", "").strip())
    ax_a.set_facecolor("#ffffff")
    ax_a.grid(axis="x", alpha=0.3)

    combo = b.team + b.engagement
    labels_combo = [c.split("_")[0] for c in combo]
    you_c = np.array([float(rows[c].mean()) for c in combo])
    bu_c = np.array([float(ctx["bu_q"][c]) for c in combo])
    xpos = np.arange(len(combo))
    w_half = 0.35

    ax_b = fig.add_subplot(gs_r[0])
    col_b = np.where(you_c >= 4.5, "#228B22", np.where(you_c >= 4.0, "#FFA500", "#C00000"))
    r1 = ax_b.bar(xpos - w_half / 2, you_c, w_half)
    ax_b.bar(xpos + w_half / 2, bu_c, w_half, hatch="//", alpha=0.65, color="#B4C7E7", edgecolor="#1F3864")
    for patch, hx in zip(r1.patches, col_b, strict=False):
        patch.set_color(hx)
    ax_b.axhline(4.0, linestyle=":", color="#777777")
    ax_b.set_xticks(xpos)
    ax_b.set_xticklabels(labels_combo, rotation=35, ha="right", fontsize=8)
    ax_b.set_title("Team + engagement bars (solid=you)")
    ax_b.set_facecolor("#ffffff")

    cum = np.zeros(len(b.leader))
    cmap_st = ["#C00000", "#FF9933", "#FFF176", "#AEEA94", "#1B7F3A"]
    ax_c = fig.add_subplot(gs_r[1])
    ystack = np.arange(len(b.leader))
    for ridx in range(5):
        rating = ridx + 1
        share = []
        for q in b.leader:
            serie = rows[q].astype(int).tolist()
            share.append(serie.count(rating) / max(len(serie), 1) * 100)
        share_arr = np.array(share)
        ax_c.barh(
            ystack,
            share_arr,
            left=cum,
            color=cmap_st[ridx],
            edgecolor="white",
            linewidth=0.35,
            label="%ss" % rating,
            height=0.65,
        )
        cum = cum + share_arr

    handles = [mpatches.Patch(color=cmap_st[i], label="%ss" % (i + 1)) for i in range(5)]
    ax_c.legend(handles=handles, ncol=5, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.2))
    ax_c.set_yticks(ystack)
    ax_c.set_yticklabels([q.split("_")[0] for q in b.leader], fontsize=8)
    ax_c.set_xlabel("% of pillar ratings")
    ax_c.set_title("Pillar mixes (counts %)")
    ax_c.set_facecolor("#ffffff")

    fig.patch.set_facecolor("#f8f9fa")
    fig.suptitle("%s pulse chart · %s · n=%s" % (manager, PERIOD, len(rows)))

    outp = (INDIV / f"{manager} - Pulse Survey Personal Report Chart.png").resolve()
    fig.subplots_adjust(bottom=0.12)
    fig.savefig(outp, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return outp


def _round_num(value: float, digits: int = 4) -> float:
    return round(float(value), digits)


def export_metrics_json(ctx: dict, path: Path, chart_paths: list[Path]) -> Path:
    """Write LLM-safe numeric payload. All figures come from analyse()."""
    dim = ctx["dim_compare"]
    dim_rows = []
    for mgr, row in dim.iterrows():
        dim_rows.append(
            {
                "manager": str(mgr),
                **{str(col): _round_num(row[col]) for col in dim.columns},
            }
        )
    payload = {
        "mode": "pulse",
        "source": str(CSV),
        "team": TEAM_NAME,
        "period": PERIOD,
        "n": int(len(ctx["df"])),
        "kpiValues": [
            {"label": "Respondents", "value": int(len(ctx["df"])), "display": str(len(ctx["df"]))},
            {
                "label": "Direct Leader (Q1–Q10)",
                "value": _round_num(ctx["bu_dl"]),
                "display": f"{ctx['bu_dl']:.2f}",
            },
            {
                "label": "Overall average",
                "value": _round_num(ctx["bu_ov"]),
                "display": f"{ctx['bu_ov']:.2f}",
            },
        ],
        "rankings": [
            {
                "manager": row["manager"],
                "n": int(row["n"]),
                "direct": _round_num(row["direct"]),
                "overall": _round_num(row["overall"]),
            }
            for row in ctx["rankings"]
        ],
        "shared_teamwide": {str(k): _round_num(v) for k, v in ctx["shared_teamwide"].items()},
        "question_means": {str(k): _round_num(v) for k, v in ctx["bu_q"].items()},
        "dimension_by_manager": dim_rows,
        "extremes": ctx["extremes_tbl"],
        "low_rates": {str(k): _round_num(v) for k, v in ctx["low_rates"].items()},
        "charts": [
            {"id": f"CH-{idx + 1}", "type": "png", "title": Path(p).name, "path": str(p)}
            for idx, p in enumerate(chart_paths)
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main() -> None:
    import argparse
    from datetime import date

    parser = argparse.ArgumentParser(description="Generate Pulse Survey team + personal PDF/PNG reports from CSV.")
    parser.add_argument("csv", type=Path, help="Path to engagement/pulse survey CSV")
    parser.add_argument("--team", default="Company", help='Team/org name (default: "Company")')
    parser.add_argument("--period", default=date.today().strftime("%Y-%m"), help="Period label YYYY-MM")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: same folder as CSV)",
    )
    parser.add_argument(
        "--no-individual",
        action="store_true",
        help="Skip personal PDFs/charts under individual_reports/",
    )
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip PDF reports; still write PNG charts (faster deck path).",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Write Python-computed metrics JSON for html-executive-deck-generation.",
    )
    args = parser.parse_args()

    global BASE, CSV, OUT_DIR, INDIV, TEAM_NAME, PERIOD
    BASE = Path(__file__).resolve().parent
    CSV = args.csv.expanduser().resolve()
    if not CSV.is_file():
        raise SystemExit(f"CSV not found: {CSV}")
    OUT_DIR = (args.out_dir.expanduser().resolve() if args.out_dir else CSV.parent)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INDIV = OUT_DIR / "individual_reports"
    TEAM_NAME = args.team
    PERIOD = args.period

    mpl_dir = OUT_DIR / ".mplconfig"
    mpl_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(mpl_dir))

    if not args.no_individual:
        INDIV.mkdir(parents=True, exist_ok=True)

    ctx = analyse()
    chart_paths: list[Path] = []
    print("Writing team artefacts…")
    if not args.no_pdf:
        tp = build_team_pdf(ctx)
        print(tp)
    cp = build_composite_png(ctx)
    chart_paths.append(Path(cp))
    print(cp)
    if not args.no_individual:
        for m in ctx["leaders"]:
            print("Personal pack:", m)
            if not args.no_pdf:
                build_personal_pdf(ctx, m)
            png = build_personal_png(ctx, m)
            chart_paths.append(Path(png))

    json_path = args.json_out
    if json_path is None:
        json_path = OUT_DIR / f"{TEAM_NAME} Pulse Survey Metrics - {PERIOD}.json"
    else:
        json_path = json_path.expanduser().resolve()
    written = export_metrics_json(ctx, json_path, chart_paths)
    print(written)


if __name__ == "__main__":
    main()

