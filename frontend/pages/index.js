import { useEffect } from 'react';
import { useRouter } from 'next/router';

import Loader from '../components/Loader';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      router.replace(user ? '/upload' : '/login');
    }
  }, [loading, router, user]);

  return <Loader label="Preparing your workspace..." />;
}
