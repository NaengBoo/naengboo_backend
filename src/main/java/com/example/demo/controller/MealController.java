package com.example.demo.controller;


import com.example.demo.domain.Meal;
import com.example.demo.service.MealService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.Optional;

@RestController
@RequestMapping("/meals")
public class MealController {

    @Autowired
    private MealService mealService;

    // 식단 추가
    @PostMapping // date(0000-00-00)와 List<MealItem> item을 받아서 저장. MealItem은 id, name, calories
    public ResponseEntity<Meal> addMeal(@RequestBody Meal meal) {
        Meal savedMeal = mealService.addMeal(meal.getDate(), meal.getItems());
        return new ResponseEntity<>(savedMeal, HttpStatus.CREATED);
    }

    // 특정 날짜의 식단 조회
    @GetMapping("/{date}")
    public ResponseEntity<Meal> getMeal(@PathVariable("date") String date) {
        Optional<Meal> meal = mealService.getMealByDate(LocalDate.parse(date));
        return meal.map(value -> new ResponseEntity<>(value, HttpStatus.OK))
                .orElseGet(() -> new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    // 식단 삭제
    @DeleteMapping("/{id}") // meal_id 를 입력 받고 해당 id의 meal 전체를 삭제
    public ResponseEntity<Void> deleteMeal(@PathVariable("id") Long id) {
        mealService.deleteMeal(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}
