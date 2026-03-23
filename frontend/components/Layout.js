import Link from 'next/link';

export default function Layout({ title, children }) {
  return (
    <div className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">MyFitnessPal CSV Analytics</p>
          <h1>{title}</h1>
        </div>
        <nav className="nav-actions">
          <Link href="/upload">Upload</Link>
          <Link href="/dashboard">Dashboard</Link>
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}
