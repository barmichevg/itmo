package ru.itmo.lab4.api;

import jakarta.validation.constraints.NotBlank;

public record HitRequest(
        @NotBlank String x,
        @NotBlank String y,
        @NotBlank String r,
        Boolean fromGraph
) {}
