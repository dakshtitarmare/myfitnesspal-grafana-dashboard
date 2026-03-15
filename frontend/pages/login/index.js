import { signInWithPopup } from 'firebase/auth';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

import Loader from '../../components/Loader';
import { useAuth } from '../../components/AuthProvider';
import { auth, googleProvider, isFirebaseConfigured } from '../../lib/firebase';

export default function LoginPage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && user) {
      router.replace('/upload');
    }
  }, [loading, router, user]);

  const handleGoogleLogin = async () => {
    if (!auth) {
      setError('Firebase environment variables are missing. Update the frontend configuration first.');
      return;
    }

    try {
      setIsSubmitting(true);
      setError('');
      await signInWithPopup(auth, googleProvider);
      localStorage.setItem(user.email);
      localStorage.setItem(user.name);
      router.push('/upload');
    } catch (loginError) {
      setError(loginError.message || 'Google sign-in failed.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return <Loader label="Loading authentication..." />;
  }

  return (
    <div className="auth-page">
      <section className="hero-card auth-card">
        <p className="eyebrow">Nutrition Intelligence</p>
        <h1>Turn MyFitnessPal exports into live Grafana dashboards.</h1>
        <p className="lead">
          Authenticate with Google, upload your CSV export, and review calories,
          macro trends, and meal patterns from PostgreSQL-backed Grafana panels.
        </p>
        <button type="button" className="primary-button" onClick={handleGoogleLogin} disabled={isSubmitting}>
          {isSubmitting ? 'Signing in...' : 'Continue with Google'}
        </button>
        {!isFirebaseConfigured && (
          <p className="hint-text">
            Firebase is not configured yet. Add the NEXT_PUBLIC_FIREBASE_* variables before testing login.
          </p>
        )}
        {error && <p className="error-text">{error}</p>}
      </section>
    </div>
  );
}
