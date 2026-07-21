'use client';

import React, { useEffect, useState } from 'react';
import { api } from '../../../lib/api';
import { Product, Lead } from '../../../types';
import { useToast } from '../../../components/Toast';

export default function LeadHunter() {
  const [products, setProducts] = useState<Product[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [hunting, setHunting] = useState(false);
  const [scoringLeadId, setScoringLeadId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const { showToast } = useToast();

  // Trade Initiation Modal State
  const [isTradeModalOpen, setIsTradeModalOpen] = useState(false);
  const [activeLead, setActiveLead] = useState<Lead | null>(null);
  const [contractValue, setContractValue] = useState('');
  const [currency, setCurrency] = useState('USD');
  const [initiatingTrade, setInitiatingTrade] = useState(false);

  const loadData = async () => {
    try {
      const [prods, discoveredLeads] = await Promise.all([
        api.products.list(),
        api.leads.list(),
      ]);
      setProducts(prods);
      setLeads(discoveredLeads);
      if (prods.length > 0) {
        setSelectedProduct(prods[0]);
      }
    } catch (err) {
      showToast('Failed to load Lead Hunter data', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleTriggerHunt = async () => {
    if (!selectedProduct) {
      showToast('Please register and select a product first', 'error');
      return;
    }
    setHunting(true);
    showToast('AI Lead Hunter engine triggered successfully!', 'info');
    try {
      await api.compute.huntLeads({
        hsCode: selectedProduct.hsCode,
        description: selectedProduct.description,
        targetRegions: selectedProduct.targetRegions,
      });
      
      // Simulate background processing delay
      setTimeout(async () => {
        const updatedLeads = await api.leads.list();
        setLeads(updatedLeads);
        setHunting(false);
        showToast('AI Lead Hunter discovered new international buyers!', 'success');
      }, 2000);
    } catch (err) {
      showToast('Failed to trigger AI Lead Hunter', 'error');
      setHunting(false);
    }
  };

  const handleScoreLead = async (leadId: string) => {
    setScoringLeadId(leadId);
    try {
      const res = await api.compute.scoreLead({ leadId });
      showToast(`Lead scored successfully! Confidence: ${res.confidenceScore}%`, 'success');
      // Refresh leads list
      const updatedLeads = await api.leads.list();
      setLeads(updatedLeads);
    } catch (err) {
      showToast('Failed to score lead', 'error');
    } finally {
      setScoringLeadId(null);
    }
  };

  const handleOpenTradeModal = (lead: Lead) => {
    setActiveLead(lead);
    setIsTradeModalOpen(true);
  };

  const handleInitiateTradeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeLead || !contractValue) return;

    setInitiatingTrade(true);
    try {
      await api.transactions.initiate({
        leadId: activeLead.id,
        contractValue: parseFloat(contractValue),
        currency,
      });
      showToast('Trade initiated! Escrow contract created.', 'success');
      setIsTradeModalOpen(false);
      setContractValue('');
      // Refresh leads list to show updated status
      const updatedLeads = await api.leads.list();
      setLeads(updatedLeads);
    } catch (err) {
      showToast('Failed to initiate trade', 'error');
    } finally {
      setInitiatingTrade(false);
    }
  };

  const getConfidenceBadgeClass = (score: number) => {
    if (score >= 80) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    if (score >= 50) return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
    return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">AI Lead Hunter</h1>
        <p className="text-slate-400 mt-1">Scrape, score, and discover verified international buyers using our FastAPI Compute Engine.</p>
      </div>

      {/* Trigger Panel */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg">
        <h3 className="text-lg font-semibold text-white mb-4">Trigger AI Lead Engine</h3>
        {products.length > 0 ? (
          <div className="flex flex-col md:flex-row items-end gap-4">
            <div className="flex-1 w-full">
              <label className="block text-sm font-medium text-slate-400 mb-1.5">Select Export Product</label>
              <select
                value={selectedProduct?.id || ''}
                onChange={(e) => {
                  const prod = products.find((p) => p.id === e.target.value);
                  if (prod) setSelectedProduct(prod);
                }}
                className="w-full px-3 py-2.5 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
              >
                {products.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} (HS: {p.hsCode})
                  </option>
                ))}
              </select>
            </div>
            <button
              onClick={handleTriggerHunt}
              disabled={hunting}
              className="w-full md:w-auto inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg font-medium text-sm transition-all shadow-lg shadow-blue-600/10 disabled:opacity-50 shrink-0"
            >
              {hunting ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Hunting Leads...
                </span>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span>Trigger AI Lead Hunter</span>
                </>
              )}
            </button>
          </div>
        ) : (
          <div className="text-center py-4">
            <p className="text-slate-400 text-sm">You must register at least one product in the catalog before triggering the Lead Hunter.</p>
          </div>
        )}
      </div>

      {/* Leads Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl shadow-lg overflow-hidden">
        <div className="p-6 border-b border-slate-800">
          <h3 className="text-lg font-semibold text-white">Discovered Leads</h3>
        </div>
        {loading ? (
          <div className="flex items-center justify-center h-48">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : leads.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-950 text-slate-400 text-xs font-semibold uppercase tracking-wider border-b border-slate-800">
                  <th className="p-4">Company Name</th>
                  <th className="p-4">Country</th>
                  <th className="p-4">Confidence Score</th>
                  <th className="p-4">Status</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-sm">
                {leads.map((lead) => (
                  <tr key={lead.id} className="hover:bg-slate-850/40 transition-colors">
                    <td className="p-4">
                      <div>
                        <p className="font-semibold text-white">{lead.companyName}</p>
                        {lead.contactEmail && <p className="text-xs text-slate-500 mt-0.5">{lead.contactEmail}</p>}
                      </div>
                    </td>
                    <td className="p-4 text-slate-300">{lead.country}</td>
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <span className={`px-2.5 py-1 text-xs font-bold rounded-full border ${getConfidenceBadgeClass(lead.confidenceScore)}`}>
                          {lead.confidenceScore.toFixed(1)}%
                        </span>
                      </div>
                    </td>
                    <td className="p-4">
                      <span className={`px-2 py-0.5 text-xs font-bold rounded border ${
                        lead.status === 'CONCLUDED'
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                          : lead.status === 'CONTACTED'
                          ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                          : lead.status === 'REJECTED'
                          ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                          : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}>
                        {lead.status}
                      </span>
                    </td>
                    <td className="p-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleScoreLead(lead.id)}
                          disabled={scoringLeadId === lead.id}
                          className="px-3 py-1.5 text-xs font-medium border border-slate-700 hover:border-slate-500 text-slate-300 rounded-lg transition-all disabled:opacity-50"
                        >
                          {scoringLeadId === lead.id ? 'Scoring...' : 'Score Lead'}
                        </button>
                        {lead.status !== 'CONCLUDED' && lead.status !== 'REJECTED' && (
                          <button
                            onClick={() => handleOpenTradeModal(lead)}
                            className="px-3 py-1.5 text-xs font-medium bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all"
                          >
                            Initiate Trade
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-12 text-center text-slate-500">No leads discovered yet. Trigger the AI Lead Hunter above to begin.</div>
        )}
      </div>

      {/* Initiate Trade Modal */}
      {isTradeModalOpen && activeLead && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full overflow-hidden shadow-2xl">
            <div className="p-6 border-b border-slate-800 flex items-center justify-between">
              <h3 className="text-xl font-bold text-white">Initiate Trade Contract</h3>
              <button
                onClick={() => setIsTradeModalOpen(false)}
                className="text-slate-400 hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <form onSubmit={handleInitiateTradeSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Counterparty Importer</label>
                <p className="text-white font-semibold text-base">{activeLead.companyName}</p>
                <p className="text-xs text-slate-500 mt-0.5">Country: {activeLead.country}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Contract Value (USD) *
                </label>
                <input
                  type="number"
                  required
                  min={1}
                  value={contractValue}
                  onChange={(e) => setContractValue(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
                  placeholder="e.g. 50000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Settlement Currency
                </label>
                <select
                  value={currency}
                  onChange={(e) => setCurrency(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
                >
                  <option value="USD">USD (United States Dollar)</option>
                  <option value="OMR">OMR (Omani Rial)</option>
                  <option value="EUR">EUR (Euro)</option>
                  <option value="AUD">AUD (Australian Dollar)</option>
                </select>
              </div>

              <div className="pt-4 border-t border-slate-800 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsTradeModalOpen(false)}
                  className="px-4 py-2 rounded-lg text-sm font-medium border border-slate-800 text-slate-400 hover:bg-slate-800 hover:text-white transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={initiatingTrade}
                  className="px-4 py-2 rounded-lg text-sm font-medium bg-blue-600 hover:bg-blue-700 text-white transition-all disabled:opacity-50"
                >
                  {initiatingTrade ? 'Initiating...' : 'Lock Escrow & Initiate'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
