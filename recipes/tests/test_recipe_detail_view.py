from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_cdetail_view_returns_404_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'Esta é uma pagina de detalhes e carrega apenas uma receita'
        # Criar uma receita
        self.make_recipe(title=needed_title)

        # Teste no content
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        # ckeca se esta receita aparece no teste
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_loads_recipe_not_publish(self):
        """ Testa se recipe ispublish é falso """
        # Criar uma receita e mudar o author desta receita, diferente do padrão carregado na inicial
        recipe = self.make_recipe(is_published=False)
        # Teste no content
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))
        self.assertEqual(response.status_code, 404)
