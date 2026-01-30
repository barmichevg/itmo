package ru.itmo.lab4.hit;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.itmo.lab4.user.UserAccount;

import java.util.List;

public interface HitRepository extends JpaRepository<Hit, Long> {
    List<Hit> findAllByUserOrderByCreatedAtDesc(UserAccount user);
    void deleteByUser(UserAccount user);
}
