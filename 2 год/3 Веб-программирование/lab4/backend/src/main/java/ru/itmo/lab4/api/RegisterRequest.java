package ru.itmo.lab4.api;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record RegisterRequest(
        @NotBlank String login,
        @NotBlank
        @Size(min = 4, max = 64)
        String password
) {}
