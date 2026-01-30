package ru.itmo.lab4.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import ru.itmo.lab4.api.ApiError;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.time.Instant;
import java.util.List;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http, ObjectMapper om) throws Exception {
        return http
                .csrf(csrf -> csrf.disable())
                .cors(cors -> {})
                .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED))
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/api/auth/**", "/actuator/health", "/actuator/info").permitAll()
                        .anyRequest().authenticated()
                )
                .exceptionHandling(eh -> eh
                        .authenticationEntryPoint((req, res, ex) -> writeJsonError(om, req.getRequestURI(), res,
                                HttpStatus.UNAUTHORIZED, "Unauthorized", List.of("Требуется авторизация")))
                        .accessDeniedHandler((req, res, ex) -> writeJsonError(om, req.getRequestURI(), res,
                                HttpStatus.FORBIDDEN, "Forbidden", List.of("Недостаточно прав")))
                )
                .build();
    }

    private static void writeJsonError(ObjectMapper om, String path, HttpServletResponse res,
                                       HttpStatus status, String message, List<String> errors) {
        try {
            res.setStatus(status.value());
            res.setCharacterEncoding("UTF-8");
            res.setContentType("application/json");

            om.writeValue(res.getOutputStream(), new ApiError(
                    Instant.now(),
                    status.value(),
                    status.getReasonPhrase(),
                    path,
                    message,
                    errors
            ));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration cfg) throws Exception {
        return cfg.getAuthenticationManager();
    }
}
