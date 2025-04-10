package com.example.demo.service;

import com.example.demo.domain.Meal;
import com.example.demo.domain.MealItem;
import com.example.demo.repository.MealRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
public class MealService {
    @Autowired
    private MealRepository mealRepository;

    public Meal addMeal(LocalDate date, List<MealItem> items) {
        Meal meal = new Meal(date, items);
        return mealRepository.save(meal);
    }

    public Optional<Meal> getMealByDate(LocalDate date) {
        return mealRepository.findByDate(date);
    }

    public void deleteMeal(Long id) {
        mealRepository.deleteById(id);
    }
}
