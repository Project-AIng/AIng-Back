package com.hansung.Aing.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.Collection;
import java.util.Collections;

@Getter
@Setter
@Entity
public class User implements UserDetails {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    private double count = 0;
    @Column
    private double gra_score;

    @Column
    private double cla_score;

    @Column
    private double coh_score;

    @Column
    private double voc_score;

    @Column
    private double str_score;

    /*@Column(length = 5000)  // 긴 텍스트를 위한 길이 지정
    private String chat_text;*/

    @Column
    private String reco_sub1;

    @Column
    private String reco_sub2;

    @Column
    private String reco_sub3;


    @Column(nullable = false)
    private String role = "ROLE_USER"; // 기본값을 설정합니다.

    private String getRole() {
        return role;
    }

    private void setRole(String role) {
        this.role = role;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return Collections.singletonList(new SimpleGrantedAuthority(getRole()));
    }

    @Override
    public String getUsername() {
        return email;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
