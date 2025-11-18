// frontend/app/layout.tsx
import "../styles/globals.css";

export const metadata = {
  title: "Asana Replica",
  description: "Home, Projects, Tasks cloned by agent",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="h-screen bg-gray-50">
        <div className="flex h-full">
          <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
            <div className="px-4 py-3 border-b">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded-full bg-[#fc636b]" />
                <div className="w-6 h-6 rounded-full bg-[#ffb900]" />
                <div className="w-6 h-6 rounded-full bg-[#3be8b0]" />
              </div>
              <p className="mt-2 font-semibold text-gray-900">Asana Replica</p>
            </div>

            <nav className="flex-1 px-3 py-4 space-y-1 text-sm">
              {/* Home link must be bold, rounded-xl, bg-gray-100 */}
              <a
                href="/"
                className="block rounded-xl px-3 py-2 font-semibold bg-gray-100 text-gray-900"
              >
                Home
              </a>
              <a
                href="/projects"
                className="block rounded-xl px-3 py-2 text-gray-700 hover:bg-gray-100"
              >
                Projects
              </a>
              <a
                href="/tasks"
                className="block rounded-xl px-3 py-2 text-gray-700 hover:bg-gray-100"
              >
                My tasks
              </a>
            </nav>
          </aside>

          <main className="flex-1 flex flex-col">
            <header className="h-14 border-b border-gray-200 flex items-center justify-between px-4">
              <h1 className="text-lg font-semibold text-gray-900">Asana Replica</h1>
              <div className="flex gap-2">
                <input
                  className="border rounded-md px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-[#1aafd0]"
                  placeholder="Search"
                />
                {/* This button is what the css.spec.ts test targets */}
                <button className="rounded-md px-3 pyJ-1 text-sm bg-[#1aafd0] text-white hover:bg-[#6a67ce]">
                + Add task
              </button>
              </div>
            </header>
            <section className="flex-1 overflow-y-auto p-6">{children}</section>
          </main>
        </div>
      </body>
    </html>
  );
}
