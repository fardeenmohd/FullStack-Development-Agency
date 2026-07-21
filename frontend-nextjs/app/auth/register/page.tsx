'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../../../context/AuthContext';
import { useToast } from '../../../components/Toast';
import { UserRole } from '../../../types';

export default function RegisterPage() {
  const { register } = useAuth();
  const { showToast } = useToast();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [role, setRole] = useState<UserRole>('EXPORTER');
  const [country, setCountry] = useState('India');
  const [iecCode, setIecCode] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // Conditional logic check
  const isIecRequired = role === 'EXPORTER' && country === 'India';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password || !companyName || !country) {
      showToast('Please fill in all required fields', 'error');
      return;
    }

    if (isIecRequired) {
      // 10-digit alphanumeric validation
      const iecRegex = /^[A-Z0-9]{10}$/i;
      if (!iecCode) {
        showToast('IEC Code is required for Indian Exporters', 'error');
        return;
      }
      if (!iecRegex.test(iecCode)) {
        showToast('IEC Code must be a 10-digit alphanumeric code', 'error');
        return;
      }
    }

    setSubmitting(true);
    try {
      await register({
        email,
        password,
        companyName,
        role,
        country,
        ...(isIecRequired ? { iecCode } : {}),
      });
      showToast('Corporate registration successful!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Registration failed. Please try again.', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4 py-12 sm:px-6 lg:px-8">
      <div className="max-w-lg w-full space-y-8 bg-slate-900 p-8 rounded-2xl border border-slate-800 shadow-2xl">
        <div>
          <div className="mx-auto h-12 w-12 bg-blue-600 rounded-xl flex items-center justify-center text-white font-bold text-xl tracking-wider">
            IN-OM
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
            Register Corporate Account
          </h2>
          <p className="mt-2 text-center text-sm text-slate-400">
            Already registered?{' '}
            <Link href="/auth/login" className="font-medium text-blue-500 hover:text-blue-400 transition-colors">
              Sign in here
            </Link>
          </p>
        </div>
        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-slate-300 mb-1">
                Corporate Email Address *
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
                placeholder="trade@company.com"
              />
            </div>

            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-slate-300 mb-1">
                Password *
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
                placeholder="••••••••"
              />
            </div>

            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-slate-300 mb-1">
                Registered Company Name *
              </label>
              <input
                type="text"
                required
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
                placeholder="Indo-Oman Trading Corp"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">
                Corporate Role *
              </label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value as UserRole)}
                className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
              >
                <option value="EXPORTER">Exporter</option>
                <option value="IMPORTER">Importer</option>
                <option value="ADMIN">Admin</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">
                Country *
              </label>
              <select
                value={country}
                onChange={(e) => setCountry(e.target.value)}
                className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
              >
                <option value="India">India</option>
                <option value="Oman">Oman</option>
                <option value="China">China</option>
                <option value="Germany">Germany</option>
                <option value="Australia">Australia</option>
              </select>
            </div>

            {isIecRequired && (
              <div className="sm:col-span-2 animate-fadeIn">
                <label className="block text-sm font-medium text-amber-400 mb-1">
                  IEC Code (Import Export Code) *
                </label>
                <input
                  type="text"
                  required
                  maxLength={10}
                  value={iecCode}
                  onChange={(e) => setIecCode(e.target.value.toUpperCase())}
                  className="w-full px-3 py-2 border border-amber-500/50 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 sm:text-sm transition-all"
                  placeholder="10-digit Alphanumeric Code"
                />
                <p className="text-xs text-slate-400 mt-1">
                  Required for Indian Exporters. Format: 10-digit alphanumeric.
                </p>
              </div>
            )}
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={submitting}
              className="w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Registering Corporate Account...
                </span>
              ) : (
                'Register Account'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
