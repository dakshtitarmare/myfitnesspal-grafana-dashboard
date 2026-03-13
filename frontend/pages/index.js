import { useEffect } from 'react';
import { useRouter } from 'next/router';

import Loader from '../components/Loader';
import { useAuth } from '../components/AuthProvider';

export default function Home() {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading) {
      router.replace(user ? '/upload' : '/login');
    }
  }, [loading, router, user]);

  return <Loader label="Preparing your workspace..." />;
}
