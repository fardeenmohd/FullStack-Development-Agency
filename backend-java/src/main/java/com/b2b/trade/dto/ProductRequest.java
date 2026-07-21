package com.b2b.trade.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import java.util.List;

public class ProductRequest {

    @NotBlank(message = "Product name is required")
    private String name;

    @NotBlank(message = "HS Code is required")
    @Size(max = 12, message = "HS Code must not exceed 12 characters")
    private String hsCode;

    @NotBlank(message = "Description is required")
    private String description;

    @NotEmpty(message = "At least one target region must be specified")
    private List<String> targetRegions;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getHsCode() {
        return hsCode;
    }

    public void setHsCode(String hsCode) {
        this.hsCode = hsCode;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public List<String> getTargetRegions() {
        return targetRegions;
    }

    public void setTargetRegions(List<String> targetRegions) {
        this.targetRegions = targetRegions;
    }
}