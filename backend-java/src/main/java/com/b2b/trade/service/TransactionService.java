package com.b2b.trade.service;

import com.b2b.trade.dto.TransactionRequest;
import com.b2b.trade.entity.Lead;
import com.b2b.trade.entity.Transaction;
import com.b2b.trade.entity.TransactionStatus;
import com.b2b.trade.entity.User;
import com.b2b.trade.exception.CustomException;
import com.b2b.trade.repository.LeadRepository;
import com.b2b.trade.repository.TransactionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class TransactionService {

    @Autowired
    private TransactionRepository transactionRepository;

    @Autowired
    private LeadRepository leadRepository;

    @Autowired
    private ComputeClientService computeClientService;

    @Transactional
    public Transaction createTransaction(TransactionRequest request, User exporter) {
        Lead lead = leadRepository.findById(request.getLeadId())
                .orElseThrow(() -> new CustomException("Lead not found", HttpStatus.NOT_FOUND));

        if (!lead.getExporter().getId().equals(exporter.getId())) {
            throw new CustomException("Unauthorized access to this lead", HttpStatus.FORBIDDEN);
        }

        Transaction transaction = new Transaction();
        transaction.setLead(lead);
        transaction.setExporter(exporter);
        transaction.setContractValue(request.getContractValue());
        transaction.setCurrency(request.getCurrency() != null ? request.getCurrency() : "USD");
        transaction.setStatus(TransactionStatus.INITIATED);

        Transaction savedTransaction = transactionRepository.save(transaction);

        // Trigger AI Lead Legitimacy and Compliance Risk Scoring asynchronously
        computeClientService.triggerScoreLead(lead.getId())
                .subscribe(null, err -> System.err.println("Failed to trigger lead scoring: " + err.getMessage()));

        return savedTransaction;
    }
}