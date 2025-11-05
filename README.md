# PhenomindUI
UI design of PhenoMind

Here’s how you can **visualize the PhenoMind clinician dashboard** I created on your laptop 👇

### 🧩 Step 1. Set up a React environment

You can either:

* **Option A:** Use an existing React project (like `create-react-app`, `Next.js`, or `Vite`), or
* **Option B:** Create a new one quickly:

  ```bash
  npx create-react-app phenomind-dashboard
  cd phenomind-dashboard
  ```

### 🧰 Step 2. Install dependencies

The dashboard uses **shadcn/ui**, **lucide-react**, **framer-motion**, and **recharts**:

```bash
npm install @radix-ui/react-tabs framer-motion lucide-react recharts class-variance-authority clsx tailwind-variants tailwindcss @radix-ui/react-tooltip
```

Then install **shadcn/ui components** (if you don’t already have them):

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add card button tabs badge progress input tooltip avatar
```

### 🎨 Step 3. Configure Tailwind CSS

If not yet initialized:

```bash
npx tailwindcss init -p
```

Then in your `tailwind.config.js`:

```js
content: ["./src/**/*.{js,jsx,ts,tsx}"],
theme: { extend: {} },
plugins: [],
```

And in your `src/index.css` (or `globals.css`):

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 📄 Step 4. Add the dashboard file

Create a new file in your `src/` folder, e.g.:

```
src/PhenoMindDashboard.jsx
```

Then paste the full React code from the canvas (titled **“PhenoMind Clinician Dashboard Mockup (React)”**).

### 🚀 Step 5. Render it

In your `App.js` (or `page.jsx` for Next.js):

```jsx
import PhenoMindDashboard from "./PhenoMindDashboard";

function App() {
  return <PhenoMindDashboard />;
}

export default App;
```

### ▶️ Step 6. Run it

```bash
npm start
```

Then open [http://localhost:3000](http://localhost:3000) — you’ll see the **PhenoMind clinician dashboard mockup** with:

* Tabs for *Patient*, *AI Insights*, *Population*
* Live demo charts (sleep, HRV, mood)
* AI risk summaries and recommendations

---

Would you like me to generate a **ready-to-run zipped project** (with the `package.json`, Tailwind config, and code pre-wired) so you can open and run it instantly?
