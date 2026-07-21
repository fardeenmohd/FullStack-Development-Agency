package com.b2b.trade.service;

import com.b2b.trade.dto.MetricsResponse;
import com.b2b.trade.entity.Transaction;
import com.b2b.trade.entity.TransactionStatus;
import com.b2b.trade.entity.User;
import com.b2b.trade.repository.LeadRepository;
import com.b2b.trade.repository.TransactionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.math.BigDecimal;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

@Service
public class DashboardService {

    @Autowired
    private LeadRepository leadRepository;

    @Autowired
    private TransactionRepository transactionRepository;

    @Transactional(readOnly = true)
    public MetricsResponse getMetrics(User user) {
        long totalActiveLeads = leadRepository.countByExporter(user);
        List<Transaction> transactions = transactionRepository.findByExporter(user);

        BigDecimal totalValue = transactions.stream()
                .map(Transaction::getContractValue)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        Map<TransactionStatus, Long> statusMap = new EnumMap<>(TransactionStatus.class);
        for (TransactionStatus status : TransactionStatus.values()) {
            statusMap.put(status, 0L);
        }

        for (Transaction tx : transactions) {
            statusMap.put(tx.getStatus(), statusMap.get(tx.getStatus()) + 1);
        }

        return new MetricsResponse(totalActiveLeads, totalValue, statusMap);
    }
}