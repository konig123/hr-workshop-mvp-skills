# Error → one student sentence

Do not paste the raw error. Say the sentence. Then follow the class in SKILL.md.

| Signal | Class | Student sentence (English) | Student sentence (Chinese) |
|---|---|---|---|
| `command not found: node` / `'node' is not recognized` | Missing Node | This computer does not have Node yet, so the web app cannot start. | 這台電腦還沒有安裝 Node，所以網頁程式還沒辦法啟動。 |
| `ENOENT` / no `package.json` | Wrong folder | Cursor is open on the wrong folder, so the command cannot find the project. | 現在開的資料夾不對，所以指令找不到專案。 |
| `EADDRINUSE` / port in use | Port in use | A development server is already running. We will use it, or open the other address it printed. | 已經有一個開發伺服器在跑。我們用它，或改用它顯示的另一個網址。 |
| `EACCES` / permission denied on install | No admin / company-locked | This computer blocked the install. That is usually a company permission setting. | 這台電腦不允許這次安裝，多半是公司權限。 |
| `npm ERR! network` / `ECONNRESET` / `ETIMEDOUT` | Network / proxy | The packages failed to download. That is the network or company firewall, not a mistake in your product. | 套件下載失敗，是網路或公司防火牆，不是產品程式寫錯。 |
| Browser cannot reach localhost, server not running | Wrong folder or Missing Node (re-check) | The local page is not running yet. I will check Node and the project folder. | 本機頁面還沒有在跑。我會先檢查 Node 和專案資料夾。 |
| Browser cannot reach localhost, server running on another port | Port in use | The app is running on a different address than 3000. Open the address in the terminal. | 應用程式在 3000 以外的網址。請打開終端機裡顯示的那個網址。 |

Terms, one sentence when first used:

- Node: the tool that lets this web app run on the computer
- npm: the tool that downloads the app's extra pieces (dependencies)
- folder: the project location Cursor currently has open
- port: the local address number in `localhost:3000`
- dependency: a piece of code the app needs, stored in `node_modules`
