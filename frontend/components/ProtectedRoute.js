import { useEffect } from 'react';
import { useRouter } from 'next/router';

import Loader from './Loader';
import { useAuth } from './AuthProvider';

export default function ProtectedRoute({ children }) {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading && !user) {
      router.replace('/login');
    }
  }, [loading, router, user]);

  if (loading || !user) {
    return <Loader label="Checking your session..." />;
  }

  return children;
}
