package com.app.model;

import jakarta.persistence.Entity;
import jakarta.validation.constraints.NotBlank;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import java.util.UUID;
import java.math.BigDecimal;
import java.sql.Timestamp;

@Entity
@Table(name = "transactions")
public class Transaction {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @NotNull(message = "Lead ID is mandatory")
    @Column(name = "lead_id", nullable = false)
    private UUID leadId;

    @NotNull(message = "Exporter ID is mandatory")
    @Column(name = "exporter_id", nullable = false)
    private UUID exporterId;

    @NotNull(message = "Contract value is mandatory")
    @Column(nullable = false)
    private BigDecimal contractValue;

    @NotBlank(message = "Currency is mandatory")
    @Column(nullable = false)
    private String currency;

    @NotNull(message = "Status is mandatory")
    @Column(nullable = false)
    private String status;

    @NotNull(message = "Updated at timestamp is mandatory")
    @Column(name = "updated_at", nullable = false, updatable = true)
    private Timestamp updatedAt;

    // Getters and Setters
}
