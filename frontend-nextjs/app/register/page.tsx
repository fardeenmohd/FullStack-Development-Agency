"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../hooks/useAuth';

export default function RegisterPage() {
  const router = useRouter();
  const { register, user } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [role, setRole] = useState('EXPORTER');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register(email, password, companyName, role);
      router.push('/login');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={handleSubmit} className="p-4 border rounded shadow-md w-96">
        <h2 className="text-xl font-bold mb-4">Register</h2>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required className="w-full p-2 mb-3 border rounded" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required className="w-full p-2 mb-4 border rounded" />
        <input type="text" value={companyName} onChange={(e) => setCompanyName(e.target.value)} placeholder="Company Name" required className="w-full p-2 mb-3 border rounded" />
        <select value={role} onChange={(e) => setRole(e.target.value)} className="w-full p-2 mb-4 border rounded">
          <option value="EXPORTER">Exporter</option>
          <option value="IMPORTER">Importer</option>
        </select>
        <button type="submit" className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">Register</button>
      </form>
    </div>
  );
}
