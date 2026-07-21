import { User, Product, Lead, Transaction, DashboardMetrics, LeadStatus, TransactionStatus } from '../types';

const CORE_API_URL = process.env.NEXT_PUBLIC_CORE_API_URL || '';
const COMPUTE_API_URL = process.env.NEXT_PUBLIC_COMPUTE_API_URL || '';

// Helper to get auth headers
const getHeaders = () => {
  if (typeof window === 'undefined') return {};
  const token = localStorage.getItem('b2b_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};

// Robust Mock Database for fallback & instant interactive demo
const initMockDB = () => {
  if (typeof window === 'undefined') return;
  
  if (!localStorage.getItem('mock_products')) {
    const initialProducts: Product[] = [
      {
        id: 'prod-1',
        exporterId: 'user-1',
        name: 'Premium Basmati Rice (1121)',
        hsCode: '10063020',
        description: 'Extra long grain aromatic Basmati rice sourced from Haryana, India.',
        targetRegions: ['OM', 'EU', 'AU'],
        createdAt: new Date().toISOString(),
      },
      {
        id: 'prod-2',
        exporterId: 'user-1',
        name: 'Organic Turmeric Powder',
        hsCode: '09103010',
        description: 'High curcumin content organic turmeric powder from Alleppey.',
        targetRegions: ['OM', 'CN', 'EU'],
        createdAt: new Date().toISOString(),
      }
    ];
    localStorage.setItem('mock_products', JSON.stringify(initialProducts));
  }

  if (!localStorage.getItem('mock_leads')) {
    const initialLeads: Lead[] = [
      {
        id: 'lead-1',
        exporterId: 'user-1',
        companyName: 'Oman Global Foods SAOC',
        country: 'Oman',
        contactEmail: 'procurement@omanglobalfoods.com',
        confidenceScore: 92.5,
        sourceUrl: 'https://omanglobalfoods.com/import-requirements',
        status: 'NEW',
        createdAt: new Date().toISOString(),
        riskAssessment: 'Low Risk. Established importer with 15+ years history.'
      },
      {
        id: 'lead-2',
        exporterId: 'user-1',
        companyName: 'EuroSpices GmbH',
        country: 'Germany',
        contactEmail: 'info@eurospices.de',
        confidenceScore: 78.2,
        sourceUrl: 'https://eurospices.de/b2b-portal',
        status: 'CONTACTED',
        createdAt: new Date().toISOString(),
        riskAssessment: 'Medium Risk. High volume buyer, strict EU pesticide compliance required.'
      },
      {
        id: 'lead-3',
        exporterId: 'user-1',
        companyName: 'Sydney Wholesale Organics',
        country: 'Australia',
        contactEmail: 'import@sydneyorganics.com.au',
        confidenceScore: 45.0,
        sourceUrl: 'https://sydneyorganics.com.au/partners',
        status: 'REJECTED',
        createdAt: new Date().toISOString(),
        riskAssessment: 'High Risk. Strict Australian biosecurity standards may delay customs clearance.'
      }
    ];
    localStorage.setItem('mock_leads', JSON.stringify(initialLeads));
  }

  if (!localStorage.getItem('mock_transactions')) {
    const initialTransactions: Transaction[] = [
      {
        id: 'tx-1',
        leadId: 'lead-2',
        exporterId: 'user-1',
        contractValue: 45000,
        currency: 'USD',
        status: 'ESCROW_LOCKED',
        updatedAt: new Date().toISOString(),
        leadCompanyName: 'EuroSpices GmbH'
      },
      {
        id: 'tx-2',
        leadId: 'lead-1',
        exporterId: 'user-1',
        contractValue: 120000,
        currency: 'USD',
        status: 'INITIATED',
        updatedAt: new Date().toISOString(),
        leadCompanyName: 'Oman Global Foods SAOC'
      }
    ];
    localStorage.setItem('mock_transactions', JSON.stringify(initialTransactions));
  }
};

initMockDB();

// Helper to read/write mock DB
const getMockData = <T>(key: string): T[] => {
  if (typeof window === 'undefined') return [];
  return JSON.parse(localStorage.getItem(key) || '[]');
};

const saveMockData = <T>(key: string, data: T[]) => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(key, JSON.stringify(data));
};

export const api = {
  // Auth Endpoints
  auth: {
    register: async (payload: any): Promise<{ token: string; user: User }> => {
      if (CORE_API_URL) {
        try {
          const res = await fetch(`${CORE_API_URL}/api/v1/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });
          if (!res.ok) throw new Error('Registration failed');
          return res.json();
        } catch (e) {
          console.warn('Core API failed, falling back to mock registration', e);
        }
      }
      
      // Mock Fallback
      const mockUser: User = {
        id: 'user-' + Math.random().toString(36).substring(2, 9),
        email: payload.email,
        companyName: payload.companyName,
        role: payload.role,
        country: payload.country,
        iecCode: payload.iecCode,
        createdAt: new Date().toISOString(),
      };
      return { token: 'mock-jwt-token-xyz', user: mockUser };
    },

    login: async (payload: any): Promise<{ token: string; user: User }> => {
      if (CORE_API_URL) {
        try {
          const res = await fetch(`${CORE_API_URL}/api/v1/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });
          if (!res.ok) throw new Error('Invalid credentials');
          return res.json();
        } catch (e) {
          console.warn('Core API failed, falling back to mock login', e);
        }
      }

      // Mock Fallback
      const mockUser: User = {
        id: 'user-1',
        email: payload.email,
        companyName: 'Indo-Oman Trading Corp',
        role: 'EXPORTER',
        country: 'India',
        iecCode: 'ABCDE1234F',
        createdAt: new Date().toISOString(),
      };
      return { token: 'mock-jwt-token-xyz', user: mockUser };
    },
  },

  // Products Endpoints
  products: {
    list: async (): Promise<Product[]> => {
      return getMockData<Product>('mock_products');
    },
    create: async (payload: Omit<Product, 'id' | 'exporterId' | 'createdAt'>): Promise<Product> => {
      if (CORE_API_URL) {
        try {
          const res = await fetch(`${CORE_API_URL}/api/v1/products`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(payload),
          });
          if (res.ok) return res.json();
        } catch (e) {
          console.warn('Core API failed, falling back to mock product creation', e);
        }
      }

      const newProduct: Product = {
        ...payload,
        id: 'prod-' + Math.random().toString(36).substring(2, 9),
        exporterId: 'user-1',
        createdAt: new Date().toISOString(),
      };
      const products = getMockData<Product>('mock_products');
      products.unshift(newProduct);
      saveMockData('mock_products', products);
      return newProduct;
    },
  },

  // Leads Endpoints
  leads: {
    list: async (): Promise<Lead[]> => {
      if (CORE_API_URL) {
        try {
          const res = await fetch(`${CORE_API_URL}/api/v1/leads`, {
            headers: getHeaders(),
          });
          if (res.ok) return res.json();
        } catch (e) {
          console.warn('Core API failed, falling back to mock leads list', e);
        }
      }
      return getMockData<Lead>('mock_leads');
    },
  },

  // Compute Engine (FastAPI)
  compute: {
    huntLeads: async (payload: { hsCode: string; description: string; targetRegions: string[] }): Promise<{ taskId: string; status: string }> => {
      if (COMPUTE_API_URL) {
        try {
          const res = await fetch(`${COMPUTE_API_URL}/api/v1/compute/hunt-leads`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(payload),
          });
          if (res.ok) return res.json();
        } catch (e) {
          console.warn('Compute API failed, falling back to mock lead hunter trigger', e);
        }
      }

      // Simulate AI Lead Hunter generating new leads in mock DB
      setTimeout(() => {
        const currentLeads = getMockData<Lead>('mock_leads');
        const regionsMap: Record<string, string> = {
          OM: 'Oman',
          CN: 'China',
          EU: 'Germany',
          AU: 'Australia'
        };
        const randomRegion = payload.targetRegions[Math.floor(Math.random() * payload.targetRegions.length)] || 'OM';
        const country = regionsMap[randomRegion] || 'Oman';
        
        const newLead: Lead = {
          id: 'lead-' + Math.random().toString(36).substring(2, 9),
          exporterId: 'user-1',
          companyName: `${country} Import-Export Alliance Ltd`,
          country: country,
          contactEmail: `trade@${country.toLowerCase().replace(' ', '')}alliance.com`,
          confidenceScore: parseFloat((60 + Math.random() * 38).toFixed(2)),
          sourceUrl: 'https://b2b-trade-directory.org/leads',
          status: 'NEW',
          createdAt: new Date().toISOString(),
          riskAssessment: 'Pending AI scoring...'
        };
        currentLeads.unshift(newLead);
        saveMockData('mock_leads', currentLeads);
      }, 1500);

      return { taskId: 'task-' + Math.random().toString(36).substring(2, 9), status: 'PENDING' };
    },

    scoreLead: async (payload: { leadId: string }): Promise<{ leadId: string; confidenceScore: number; riskAssessment: string }> => {
      if (COMPUTE_API_URL) {
        try {
          const res = await fetch(`${COMPUTE_API_URL}/api/v1/compute/score-lead`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(payload),
          });
          if (res.ok) return res.json();
        } catch (e) {
          console.warn('Compute API failed, falling back to mock lead scoring', e);
        }
      }

      // Mock scoring logic
      const leads = getMockData<Lead>('mock_leads');
      const leadIndex = leads.findIndex(l => l.id === payload.leadId);
      let score = 85.5;
      let risk = 'Low Risk. Verified trade license and active customs history.';
      
      if (leadIndex !== -1) {
        score = parseFloat((50 + Math.random() * 48).toFixed(2));
        risk = score > 80 
          ? 'Low Risk. Excellent credit rating and verified import history.' 
          : score > 50 
          ? 'Medium Risk. Moderate trade volume, standard compliance checks recommended.' 
          : 'High Risk. Limited public trade records, strict escrow terms advised.';
        
        leads[leadIndex].confidenceScore = score;
        leads[leadIndex].riskAssessment = risk;
        saveMockData('mock_leads', leads);
      }

      return { leadId: payload.leadId, confidenceScore: score, riskAssessment: risk };
    }
  },

  // Transactions Endpoints
  transactions: {
    list: async (): Promise<Transaction[]> => {
      return getMockData<Transaction>('mock_transactions');
    },
    initiate: async (payload: { leadId: string; contractValue: number; currency: string }): Promise<Transaction> => {
      if (CORE_API_URL) {
        try {
          const res = await fetch(`${CORE_API_URL}/api/v1/transactions`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(payload),
          });
          if (res.ok) return res.json();
        } catch (e) {
          console.warn('Core API failed, falling back to mock transaction initiation', e);
        }
      }

      const leads = getMockData<Lead>('mock_leads');
      const targetLead = leads.find(l => l.id === payload.leadId);
      
      const newTx: Transaction = {
        id: 'tx-' + Math.random().toString(36).substring(2, 9),
        leadId: payload.leadId,
        exporterId: 'user-1',
        contractValue: payload.contractValue,
        currency: payload.currency || 'USD',
        status: 'INITIATED',
        updatedAt: new Date().toISOString(),
        leadCompanyName: targetLead ? targetLead.companyName : 'Unknown Importer'
      };

      const txs = getMockData<Transaction>('mock_transactions');
      txs.unshift(newTx);
      saveMockData('mock_transactions', txs);

      // Update lead status to CONTACTED/CONCLUDED
      if (targetLead) {
        targetLead.status = 'CONCLUDED';
        saveMockData('mock_leads', leads);
      }

      return newTx;
    },
    updateStatus: async (txId: string, status: TransactionStatus): Promise<Transaction> => {
      const txs = getMockData<Transaction>('mock_transactions');
      const index = txs.findIndex(t => t.id === txId);
      if (index !== -1) {
        txs[index].status = status;
        txs[index].updatedAt = new Date().toISOString();
        saveMockData('mock_transactions', txs);
        return txs[index];
      }
      throw new Error('Transaction not found');
    }
  },

  // Dashboard Metrics
  dashboard: {
    getMetrics: async (): Promise<DashboardMetrics> => {
      if (CORE_API_URL) {
        try {
          const res = await fetch(`${CORE_API_URL}/api/v1/dashboard/metrics`, {
            headers: getHeaders(),
          });
          if (res.ok) return res.json();
        } catch (e) {
          console.warn('Core API failed, falling back to mock metrics calculation', e);
        }
      }

      const leads = getMockData<Lead>('mock_leads');
      const txs = getMockData<Transaction>('mock_transactions');

      const totalActiveLeads = leads.filter(l => l.status !== 'REJECTED').length;
      const totalTransactionValue = txs.reduce((sum, t) => sum + t.contractValue, 0);
      const pendingEscrows = txs.filter(t => t.status === 'ESCROW_LOCKED').length;
      const successfulTrades = txs.filter(t => t.status === 'COMPLETED').length;

      const leadsByStatus = leads.reduce((acc, lead) => {
        acc[lead.status] = (acc[lead.status] || 0) + 1;
        return acc;
      }, { NEW: 0, CONTACTED: 0, CONCLUDED: 0, REJECTED: 0 } as Record<LeadStatus, number>);

      return {
        totalActiveLeads,
        totalTransactionValue,
        pendingEscrows,
        successfulTrades,
        leadsByStatus,
        recentTransactions: txs.slice(0, 5),
      };
    }
  }
};
