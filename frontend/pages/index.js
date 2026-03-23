import { useEffect } from 'react';
import { useRouter } from 'next/router';

import Loader from '../components/Loader';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/upload');
  }, [router]);

  return <Loader label="Preparing your workspace..." />;
}
