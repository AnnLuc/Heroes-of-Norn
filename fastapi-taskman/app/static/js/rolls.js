// app/static/js/rolls.js

// Выполнение броска кубика
async function roll(characterId, attribute, skill, resultElement) {
  try {
    const response = await fetch(`/characters/roll/${characterId}/${attribute}/${skill}`);
    if (!response.ok) throw new Error("Ошибка при получении результата броска");

    const result = await response.json();
    console.log(`Результат броска для ${attribute} с навыком ${skill}:`, result);

    if (resultElement) {
      resultElement.textContent = `🎲 ${result.result}`;
    }
  } catch (error) {
    console.error("Ошибка броска:", error);
    if (resultElement) {
      resultElement.textContent = "⚠ Ошибка!";
    }
  }
}

// Назначение обработчиков всем кнопкам бросков
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".roll-button");
  if (buttons.length > 0) {
    buttons.forEach(button => {
      button.addEventListener("click", async () => {
        const characterId = button.dataset.characterId;
        const attribute = button.dataset.attribute;
        const skill = button.dataset.skill;
        const resultElement = button.parentElement.querySelector(".roll-result"); // предполагаем, что рядом элемент для вывода

        await roll(characterId, attribute, skill, resultElement);
      });
    });
  } else {
    console.warn("Нет кнопок с классом .roll-button на странице.");
  }
});
