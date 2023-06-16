from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1> Não existem receitas disponíveis ! </h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # Criar uma receita e mudar o author desta receita, diferente do padrão carregado na inicial
        self.make_recipe(author_data={
            'first_name': 'João dos Santos'
        })
        # Teste no Context
        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes']
        self.assertEqual(
            response_recipes.first().preparation_time_unit, 'minutos')

        # Teste no content
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        # ckeca se estes dados aparecem no teste
        self.assertIn('recipe-description', content)
        self.assertIn('10 minutos', content)
        self.assertIn('2 pessoas', content)
        self.assertIn('João dos Santos', content)

    def test_recipe_home_template_loads_recipes_not_publish(self):
        """ Testa se recipe ispublish é falso """
        # Criar uma receita e mudar o author desta receita, diferente do padrão carregado na inicial
        self.make_recipe(is_published=False)
        # Teste no content
        response = self.client.get(reverse('recipes:home'))
        # ckeca se não tem receita
        self.assertIn(
            '<h1> Não existem receitas disponíveis ! </h1>',
            response.content.decode('utf-8')
        )
