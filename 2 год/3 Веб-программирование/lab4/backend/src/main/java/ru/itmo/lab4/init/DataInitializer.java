package ru.itmo.lab4.init;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;
import ru.itmo.lab4.user.UserAccount;
import ru.itmo.lab4.user.UserRepository;

@Configuration
public class DataInitializer {

    @Bean
    public CommandLineRunner initUsers(UserRepository userRepository, PasswordEncoder encoder) {
        return args -> {
            if (!userRepository.existsByLogin("admin")) {
                String hash = encoder.encode("admin");
                userRepository.save(new UserAccount("admin", hash));
            }
        };
    }
}
