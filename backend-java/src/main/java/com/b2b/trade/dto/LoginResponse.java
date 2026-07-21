package com.b2b.trade.dto;

import com.b2b.trade.entity.Role;

public class LoginResponse {
    private String token;
    private String email;
    private String companyName;
    private Role role;

    public LoginResponse(String token, String email, String companyName, Role role) {
        this.token = token;
        this.email = email;
        this.companyName = companyName;
        this.role = role;
    }

    public String getToken() {
        return token;
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
}