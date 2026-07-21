'use client';

import React, { useEffect, useState } from 'react';
import { api } from '../../../lib/api';
import { Transaction, TransactionStatus } from '../../../types';
import { useToast } from '../../../components/Toast';

const STAGES: TransactionStatus[] = ['INITIATED', 'ESCROW_LOCKED', 'SHIPPED', 'DELIVERED', 'COMPLETED'];

export default function EscrowTracker() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const { showToast } = useToast();

  const fetchTransactions = async () => {
    try {
      const data = await api.transactions.list();
      setTransactions(data);
    } catch (err) {
      showToast('Failed to load transactions', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleAdvanceStatus = async (txId: string, currentStatus: TransactionStatus) => {
    const currentIndex = STAGES.indexOf(currentStatus);
    if (currentIndex === -1 || currentIndex === STAGES.length - 1) return;

    const nextStatus = STAGES[currentIndex + 1];
    try {
      await api.transactions.updateStatus(txId, nextStatus);
      showToast(`Transaction advanced to ${nextStatus}`, 'success');
      fetchTransactions();
    } catch (err) {
      showToast('Failed to update transaction status', 'error');
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">Escrow & Trade Tracker</h1>
        <p className="text-slate-400 mt-1">Monitor active trade milestones, secure escrow locks, and shipping status.</p>
      </div>

      {/* Transactions List */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : transactions.length > 0 ? (
        <div className="space-y-6">
          {transactions.map((tx) => {
            const activeIndex = STAGES.indexOf(tx.status);
            return (
              <div key={tx.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-6">
                {/* Top Info Row */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/60 pb-4">
                  <div>
                    <h3 className="text-lg font-bold text-white">{tx.leadCompanyName || 'Global Importer'}</h3>
                    <p className="text-xs text-slate-500 mt-0.5">Transaction ID: {tx.id} • Last Updated: {new Date(tx.updatedAt).toLocaleString()}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-left sm:text-right">
                      <p className="text-lg font-bold text-emerald-400">${tx.contractValue.toLocaleString()} {tx.currency}</p>
                      <p className="text-xs text-slate-500">Contract Value</p>
                    </div>
                    {tx.status !== 'COMPLETED' && (
                      <button
                        onClick={() => handleAdvanceStatus(tx.id, tx.status)}
                        className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg transition-all shadow-lg shadow-blue-600/10"
                      >
                        Advance Stage
                      </button>
                    )}
                  </div>
                </div>

                {/* Visual Stepper */}
                <div className="relative">
                  {/* Progress Line Background */}
                  <div className="absolute top-5 left-4 right-4 h-0.5 bg-slate-800 -z-10"></div>
                  {/* Active Progress Line */}
                  <div
                    className="absolute top-5 left-4 h-0.5 bg-blue-500 -z-10 transition-all duration-500"
                    style={{ width: `${(activeIndex / (STAGES.length - 1)) * 100}%` }}
                  ></div>

                  <div className="grid grid-cols-5 gap-2">
                    {STAGES.map((stage, idx) => {
                      const isCompleted = idx < activeIndex;
                      const isActive = idx === activeIndex;
                      const isPending = idx > activeIndex;

                      return (
                        <div key={stage} className="flex flex-col items-center text-center">
                          <div
                            className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${
                              isCompleted
                                ? 'bg-blue-600 border-blue-500 text-white'
                                : isActive
                                ? 'bg-slate-900 border-blue-500 text-blue-400 shadow-lg shadow-blue-500/20'
                                : 'bg-slate-950 border-slate-800 text-slate-600'
                            }`}
                          >
                            {isCompleted ? (
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 13l4 4L19 7" />
                              </svg>
                            ) : (
                              <span className="text-xs font-bold">{idx + 1}</span>
                            )}
                          </div>
                          <p className={`text-[10px] sm:text-xs font-bold mt-2.5 uppercase tracking-wider ${
                            isActive ? 'text-blue-400' : isCompleted ? 'text-slate-300' : 'text-slate-600'
                          }`}>
                            {stage.replace('_', ' ')}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center">
          <svg className="w-12 h-12 text-slate-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <h3 className="text-lg font-semibold text-white">No Active Trades</h3>
          <p className="text-slate-400 mt-1 max-w-md mx-auto">Initiate a trade contract with discovered buyers in the AI Lead Hunter panel to start tracking escrows.</p>
        </div>
      )}
    </div>
  );
}
