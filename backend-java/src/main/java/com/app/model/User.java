package com.app.model;

import jakarta.persistence.Entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.UUID;
import java.sql.Timestamp;

@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @NotBlank(message = "Email is mandatory")
    @Email(message = "Invalid email format")
    @Column(unique = true, nullable = false)
    private String email;

    @NotBlank(message = "Password hash is mandatory")
    @Column(nullable = false)
    private String passwordHash;

    @NotBlank(message = "Company name is mandatory")
    @Column(nullable = false)
    private String companyName;

    @NotNull(message = "Role is mandatory")
    @Column(nullable = false)
    private String role;

    @NotBlank(message = "Country is mandatory")
    @Column(nullable = false)
    private String country;

    @Column(name = "iec_code")
    private String iecCode;

    @NotNull(message = "Created at timestamp is mandatory")
    @Column(name = "created_at", nullable = false, updatable = false)
    private Timestamp createdAt;

    // Getters and Setters
}
