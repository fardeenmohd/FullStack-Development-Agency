package com.b2b.trade.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;
import java.util.UUID;

public class TransactionRequest {

    @NotNull(message = "Lead ID is required")
    private UUID leadId;

    @NotNull(message = "Contract value is required")
    private BigDecimal contractValue;

    @Size(max = 3, message = "Currency code must be at most 3 characters")
    private String currency = "USD";

    public UUID getLeadId() {
        return leadId;
    }

    public void setLeadId(UUID leadId) {
        this.leadId = leadId;
    }

    public BigDecimal getContractValue() {
        return contractValue;
    }

    public void setContractValue(BigDecimal contractValue) {
        this.contractValue = contractValue;
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
    }
}