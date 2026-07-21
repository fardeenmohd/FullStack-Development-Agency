"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../hooks/useAuth';
import { useDashboardMetrics } from '../hooks/useDashboardMetrics';
import { Dashboard } from '../components/Dashboard';

export default function Home() {
  const router = useRouter();
  const { user, login } = useAuth();
  const { metrics, isLoading, error } = useDashboardMetrics();

  useEffect(() => {
    if (!user) {
      router.push('/login');
    }
  }, [user, router]);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <Dashboard metrics={metrics} />
  );
}
