package com.b2b.trade.dto;

import com.b2b.trade.entity.TransactionStatus;
import java.math.BigDecimal;
import java.util.Map;

public class MetricsResponse {
    private long totalActiveLeads;
    private BigDecimal totalTransactionValue;
    private Map<TransactionStatus, Long> transactionsByStatus;

    public MetricsResponse(long totalActiveLeads, BigDecimal totalTransactionValue, Map<TransactionStatus, Long> transactionsByStatus) {
        this.totalActiveLeads = totalActiveLeads;
        this.totalTransactionValue = totalTransactionValue;
        this.transactionsByStatus = transactionsByStatus;
    }

    public long getTotalActiveLeads() {
        return totalActiveLeads;
    }

    public BigDecimal getTotalTransactionValue() {
        return totalTransactionValue;
    }

    public Map<TransactionStatus, Long> getTransactionsByStatus() {
        return transactionsByStatus;
    }
}