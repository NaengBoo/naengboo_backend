package com.example.demo.domain;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
public class Meal {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private LocalDate date;

    @OneToMany(cascade = CascadeType.ALL)
    @JoinColumn(name = "meal_id")
    private List<MealItem> items = new ArrayList<>();


    public Meal() {}

    public Meal(LocalDate date, List<MealItem> items) {
        this.date = date;
        this.items = items;
    }


    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public List<MealItem> getItems() {
        return items;
    }

    public void setItems(List<MealItem> items) {
        this.items = items;
    }
}
