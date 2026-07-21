'use client';

import React, { useEffect, useState } from 'react';
import { api } from '../../../lib/api';
import { Product } from '../../../types';
import { useToast } from '../../../components/Toast';

export default function ProductCatalog() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { showToast } = useToast();

  // Form State
  const [name, setName] = useState('');
  const [hsCode, setHsCode] = useState('');
  const [description, setDescription] = useState('');
  const [targetRegions, setTargetRegions] = useState<('OM' | 'CN' | 'EU' | 'AU')[]>([]);
  const [submitting, setSubmitting] = useState(false);

  const fetchProducts = async () => {
    try {
      const data = await api.products.list();
      setProducts(data);
    } catch (err) {
      showToast('Failed to load products', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleRegionToggle = (region: 'OM' | 'CN' | 'EU' | 'AU') => {
    if (targetRegions.includes(region)) {
      setTargetRegions(targetRegions.filter((r) => r !== region));
    } else {
      setTargetRegions([...targetRegions, region]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // HS Code Validation: numeric, 6 to 12 digits
    const hsCodeRegex = /^[0-9]{6,12}$/;
    if (!hsCodeRegex.test(hsCode)) {
      showToast('HS Code must be numeric and between 6 to 12 digits', 'error');
      return;
    }

    if (targetRegions.length === 0) {
      showToast('Please select at least one target region', 'error');
      return;
    }

    setSubmitting(true);
    try {
      await api.products.create({
        name,
        hsCode,
        description,
        targetRegions,
      });
      showToast('Product registered successfully!', 'success');
      setIsModalOpen(false);
      // Reset Form
      setName('');
      setHsCode('');
      setDescription('');
      setTargetRegions([]);
      fetchProducts();
    } catch (err) {
      showToast('Failed to register product', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Product Catalog</h1>
          <p className="text-slate-400 mt-1">Manage your export products and target international markets.</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-lg font-medium text-sm transition-all shadow-lg shadow-blue-600/10 self-start sm:self-auto"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>Add Product</span>
        </button>
      </div>

      {/* Product Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : products.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <div key={product.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg flex flex-col justify-between hover:border-slate-700 transition-all">
              <div>
                <div className="flex items-start justify-between gap-2">
                  <h3 className="text-lg font-bold text-white line-clamp-1">{product.name}</h3>
                  <span className="px-2.5 py-1 text-xs font-mono font-bold bg-slate-850 text-blue-400 border border-slate-800 rounded">
                    HS {product.hsCode}
                  </span>
                </div>
                <p className="text-sm text-slate-400 mt-3 line-clamp-3">{product.description}</p>
              </div>
              <div className="mt-6 pt-4 border-t border-slate-800/60">
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Target Regions</p>
                <div className="flex flex-wrap gap-1.5">
                  {product.targetRegions.map((region) => (
                    <span
                      key={region}
                      className="px-2 py-0.5 text-xs font-bold bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded"
                    >
                      {region === 'OM' ? 'Oman' : region === 'CN' ? 'China' : region === 'EU' ? 'Europe' : 'Australia'}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center">
          <svg className="w-12 h-12 text-slate-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
          <h3 className="text-lg font-semibold text-white">No Products Registered</h3>
          <p className="text-slate-400 mt-1 max-w-md mx-auto">Register your export products to start hunting for international leads using our AI engine.</p>
          <button
            onClick={() => setIsModalOpen(true)}
            className="mt-6 inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm transition-all"
          >
            Add Your First Product
          </button>
        </div>
      )}

      {/* Add Product Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full overflow-hidden shadow-2xl animate-scaleIn">
            <div className="p-6 border-b border-slate-800 flex items-center justify-between">
              <h3 className="text-xl font-bold text-white">Register Export Product</h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-white transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Product Name *
                </label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
                  placeholder="e.g. Premium Basmati Rice"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  HS Code (Harmonized System Code) *
                </label>
                <input
                  type="text"
                  required
                  value={hsCode}
                  onChange={(e) => setHsCode(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
                  placeholder="6 to 12 digit numeric code"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">
                  Product Description *
                </label>
                <textarea
                  required
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-700 text-white rounded-lg bg-slate-950 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
                  placeholder="Describe quality, packaging, origin, and certifications..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Target Regions (Select at least one) *
                </label>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { code: 'OM', label: 'Oman' },
                    { code: 'CN', label: 'China' },
                    { code: 'EU', label: 'Europe' },
                    { code: 'AU', label: 'Australia' },
                  ].map((region) => {
                    const isSelected = targetRegions.includes(region.code as any);
                    return (
                      <button
                        type="button"
                        key={region.code}
                        onClick={() => handleRegionToggle(region.code as any)}
                        className={`flex items-center justify-between p-3 rounded-lg border text-sm font-medium transition-all ${
                          isSelected
                            ? 'bg-blue-600/10 border-blue-500 text-blue-400'
                            : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
                        }`}
                      >
                        <span>{region.label}</span>
                        {isSelected && (
                          <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 rounded-lg text-sm font-medium border border-slate-800 text-slate-400 hover:bg-slate-800 hover:text-white transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 rounded-lg text-sm font-medium bg-blue-600 hover:bg-blue-700 text-white transition-all disabled:opacity-50"
                >
                  {submitting ? 'Registering...' : 'Register Product'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
