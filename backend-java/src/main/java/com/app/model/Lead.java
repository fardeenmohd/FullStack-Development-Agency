package com.app.model;

import jakarta.persistence.Entity;
import java.math.BigDecimal;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.UUID;
import java.sql.Timestamp;

@Entity
@Table(name = "leads")
public class Lead {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @NotNull(message = "Exporter ID is mandatory")
    @Column(name = "exporter_id", nullable = false)
    private UUID exporterId;

    @NotBlank(message = "Company name is mandatory")
    @Column(nullable = false)
    private String companyName;

    @NotBlank(message = "Country is mandatory")
    @Column(nullable = false)
    private String country;

    @Column(name = "contact_email")
    private String contactEmail;

    @NotNull(message = "Confidence score is mandatory")
    @Column(nullable = false)
    private BigDecimal confidenceScore;

    @Column(name = "source_url")
    private String sourceUrl;

    @NotNull(message = "Status is mandatory")
    @Column(nullable = false)
    private String status;

    @NotNull(message = "Created at timestamp is mandatory")
    @Column(name = "created_at", nullable = false, updatable = false)
    private Timestamp createdAt;

    // Getters and Setters
}
