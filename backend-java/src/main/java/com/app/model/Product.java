package com.app.model;

import jakarta.persistence.Entity;
import java.util.List;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.UUID;
import java.sql.Timestamp;

@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @NotNull(message = "Exporter ID is mandatory")
    @Column(name = "exporter_id", nullable = false)
    private UUID exporterId;

    @NotBlank(message = "Product name is mandatory")
    @Column(nullable = false)
    private String name;

    @NotBlank(message = "HS code is mandatory")
    @Column(nullable = false)
    private String hsCode;

    @NotBlank(message = "Description is mandatory")
    @Column(nullable = false)
    private String description;

    @NotNull(message = "Target regions are mandatory")
    @Column(name = "target_regions", nullable = false)
    private List<String> targetRegions;

    @NotNull(message = "Created at timestamp is mandatory")
    @Column(name = "created_at", nullable = false, updatable = false)
    private Timestamp createdAt;

    // Getters and Setters
}
