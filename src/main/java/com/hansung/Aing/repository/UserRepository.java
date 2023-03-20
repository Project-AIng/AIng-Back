package com.hansung.Aing.repository;
import org.springframework.data.jpa.repository.JpaRepository;
import com.hansung.Aing.model.User;

public interface UserRepository extends JpaRepository<User, Long> {
    boolean existsByName(String name);

    boolean existsByEmail(String email);

    User findByName(String name);

    User findByEmail(String email);

    User findByEmailAndPassword(String email, String password);
}

