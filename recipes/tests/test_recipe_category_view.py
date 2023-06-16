from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'Esta é uma receita teste'
        # Criar uma receita
        self.make_recipe(title=needed_title)

        # Teste no content
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        # ckeca se esta receita aparece no teste
        self.assertIn(needed_title, content)

    def test_recipe_category_template_loads_recipes_not_publish(self):
        """ Testa se recipe ispublish é falso """
        # Criar uma receita e mudar o author desta receita, diferente do padrão carregado na inicial
        recipe = self.make_recipe(is_published=False)
        # Teste no content
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id}))
        self.assertEqual(response.status_code, 404)
