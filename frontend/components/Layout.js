import { signOut } from 'firebase/auth';
import Link from 'next/link';
import { useRouter } from 'next/router';

import { useAuth } from './AuthProvider';
import { auth } from '../lib/firebase';

export default function Layout({ title, children }) {
  const router = useRouter();
  const { user } = useAuth();

  const handleSignOut = async () => {
    if (auth) {
      await signOut(auth);
    }
    router.push('/login');
  };

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
          {user && <span className="user-pill">{user.displayName || user.email}</span>}
          <button type="button" className="ghost-button" onClick={handleSignOut}>
            Sign out
          </button>
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}
