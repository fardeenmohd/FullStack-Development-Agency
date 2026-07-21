package com.b2b.trade.controller;

import com.b2b.trade.config.CustomUserDetails;
import com.b2b.trade.dto.TransactionRequest;
import com.b2b.trade.entity.Transaction;
import com.b2b.trade.service.TransactionService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/transactions")
public class TransactionController {

    @Autowired
    private TransactionService transactionService;

    @PostMapping
    @PreAuthorize("hasRole('EXPORTER')")
    public ResponseEntity<Transaction> createTransaction(
            @Valid @RequestBody TransactionRequest request,
            @AuthenticationPrincipal CustomUserDetails userDetails) {
        Transaction transaction = transactionService.createTransaction(request, userDetails.getUser());
        return new ResponseEntity<>(transaction, HttpStatus.CREATED);
    }
}