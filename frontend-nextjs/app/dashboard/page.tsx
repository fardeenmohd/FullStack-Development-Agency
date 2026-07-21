'use client';

import React, { useEffect, useState } from 'react';
import { api } from '../../lib/api';
import { DashboardMetrics } from '../../types';
import { useToast } from '../../components/Toast';

export default function DashboardOverview() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const { showToast } = useToast();

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await api.dashboard.getMetrics();
        setMetrics(data);
      } catch (err) {
        showToast('Failed to load dashboard metrics', 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, [showToast]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">Dashboard Overview</h1>
        <p className="text-slate-400 mt-1">Real-time trade metrics, active escrows, and lead pipelines.</p>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-slate-400 uppercase tracking-wider">Active Leads</p>
            <h3 className="text-3xl font-bold text-white mt-2">{metrics?.totalActiveLeads || 0}</h3>
          </div>
          <div className="p-3 bg-blue-500/10 text-blue-400 rounded-lg">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-slate-400 uppercase tracking-wider">Total Trade Value</p>
            <h3 className="text-3xl font-bold text-emerald-400 mt-2">
              ${metrics?.totalTransactionValue.toLocaleString() || 0}
            </h3>
          </div>
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-lg">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-slate-400 uppercase tracking-wider">Pending Escrows</p>
            <h3 className="text-3xl font-bold text-amber-400 mt-2">{metrics?.pendingEscrows || 0}</h3>
          </div>
          <div className="p-3 bg-amber-500/10 text-amber-400 rounded-lg">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-slate-400 uppercase tracking-wider">Successful Trades</p>
            <h3 className="text-3xl font-bold text-blue-400 mt-2">{metrics?.successfulTrades || 0}</h3>
          </div>
          <div className="p-3 bg-blue-500/10 text-blue-400 rounded-lg">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      {/* Charts & Lead Conversion Pipeline */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg lg:col-span-2">
          <h3 className="text-lg font-semibold text-white mb-4">Lead Conversion Rates</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-400">New Leads Discovered</span>
                <span className="text-white font-semibold">{metrics?.leadsByStatus.NEW || 0}</span>
              </div>
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                <div className="bg-blue-500 h-full rounded-full" style={{ width: `${((metrics?.leadsByStatus.NEW || 0) / (metrics?.totalActiveLeads || 1)) * 100}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-400">Contacted / In Negotiation</span>
                <span className="text-white font-semibold">{metrics?.leadsByStatus.CONTACTED || 0}</span>
              </div>
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                <div className="bg-amber-500 h-full rounded-full" style={{ width: `${((metrics?.leadsByStatus.CONTACTED || 0) / (metrics?.totalActiveLeads || 1)) * 100}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-400">Concluded Trades</span>
                <span className="text-white font-semibold">{metrics?.leadsByStatus.CONCLUDED || 0}</span>
              </div>
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${((metrics?.leadsByStatus.CONCLUDED || 0) / (metrics?.totalActiveLeads || 1)) * 100}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-400">Rejected / Disqualified</span>
                <span className="text-white font-semibold">{metrics?.leadsByStatus.REJECTED || 0}</span>
              </div>
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                <div className="bg-rose-500 h-full rounded-full" style={{ width: `${((metrics?.leadsByStatus.REJECTED || 0) / (metrics?.totalActiveLeads || 1)) * 100}%` }}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-semibold text-white mb-4">Target Regions Distribution</h3>
          <div className="flex flex-col gap-4">
            <div className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-800">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-blue-500"></span>
                <span className="text-sm font-medium text-slate-300">Oman (OM)</span>
              </div>
              <span className="text-xs font-bold text-slate-400">High Demand</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-800">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
                <span className="text-sm font-medium text-slate-300">Europe (EU)</span>
              </div>
              <span className="text-xs font-bold text-slate-400">Strict Compliance</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-800">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-amber-500"></span>
                <span className="text-sm font-medium text-slate-300">Australia (AU)</span>
              </div>
              <span className="text-xs font-bold text-slate-400">Biosecurity Focus</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-800">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-purple-500"></span>
                <span className="text-sm font-medium text-slate-300">China (CN)</span>
              </div>
              <span className="text-xs font-bold text-slate-400">Bulk Volume</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Transactions Feed */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl shadow-lg overflow-hidden">
        <div className="p-6 border-b border-slate-800">
          <h3 className="text-lg font-semibold text-white">Recent Transactions</h3>
        </div>
        <div className="divide-y divide-slate-800">
          {metrics?.recentTransactions && metrics.recentTransactions.length > 0 ? (
            metrics.recentTransactions.map((tx) => (
              <div key={tx.id} className="p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-850 transition-colors">
                <div>
                  <h4 className="text-sm font-semibold text-white">{tx.leadCompanyName || 'Global Importer'}</h4>
                  <p className="text-xs text-slate-400 mt-1">ID: {tx.id} • Updated: {new Date(tx.updatedAt).toLocaleDateString()}</p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className="text-sm font-bold text-white">${tx.contractValue.toLocaleString()} {tx.currency}</p>
                    <p className="text-xs text-slate-500">Escrow Value</p>
                  </div>
                  <span className={`px-2.5 py-1 text-xs font-bold rounded-full border ${
                    tx.status === 'COMPLETED'
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                      : tx.status === 'ESCROW_LOCKED'
                      ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                      : 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                  }`}>
                    {tx.status}
                  </span>
                </div>
              </div>
            ))
          ) : (
            <div className="p-6 text-center text-slate-500 text-sm">No transactions initiated yet.</div>
          )}
        </div>
      </div>
    </div>
  );
}
