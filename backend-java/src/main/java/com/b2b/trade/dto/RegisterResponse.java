package com.b2b.trade.dto;

import com.b2b.trade.entity.Role;
import java.time.Instant;
import java.util.UUID;

public class RegisterResponse {
    private UUID id;
    private String email;
    private String companyName;
    private Role role;
    private String country;
    private String iecCode;
    private Instant createdAt;

    public RegisterResponse(UUID id, String email, String companyName, Role role, String country, String iecCode, Instant createdAt) {
        this.id = id;
        this.email = email;
        this.companyName = companyName;
        this.role = role;
        this.country = country;
        this.iecCode = iecCode;
        this.createdAt = createdAt;
    }

    public UUID getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public String getCompanyName() {
        return companyName;
    }

    public Role getRole() {
        return role;
    }

    public String getCountry() {
        return country;
    }

    public String getIecCode() {
        return iecCode;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}