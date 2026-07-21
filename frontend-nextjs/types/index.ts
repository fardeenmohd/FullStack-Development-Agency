export type UserRole = 'EXPORTER' | 'IMPORTER' | 'ADMIN';

export interface User {
  id: string;
  email: string;
  companyName: string;
  role: UserRole;
  country: string;
  iecCode?: string; // Required if role is EXPORTER and country is India
  createdAt: string;
}

export interface Product {
  id: string;
  exporterId: string;
  name: string;
  hsCode: string; // Harmonized System Code (up to 12 chars)
  description: string;
  targetRegions: ('OM' | 'CN' | 'EU' | 'AU')[];
  createdAt: string;
}

export type LeadStatus = 'NEW' | 'CONTACTED' | 'CONCLUDED' | 'REJECTED';

export interface Lead {
  id: string;
  exporterId: string;
  companyName: string;
  country: string;
  contactEmail?: string;
  confidenceScore: number; // Decimal/Float up to 100.00
  sourceUrl?: string;
  status: LeadStatus;
  createdAt: string;
  riskAssessment?: string;
}

export type TransactionStatus = 'INITIATED' | 'ESCROW_LOCKED' | 'SHIPPED' | 'DELIVERED' | 'COMPLETED';

export interface Transaction {
  id: string;
  leadId: string;
  exporterId: string;
  contractValue: number;
  currency: string; // Default 'USD'
  status: TransactionStatus;
  updatedAt: string;
  leadCompanyName?: string;
}

export interface DashboardMetrics {
  totalActiveLeads: number;
  totalTransactionValue: number;
  pendingEscrows: number;
  successfulTrades: number;
  leadsByStatus: Record<LeadStatus, number>;
  recentTransactions: Transaction[];
}
