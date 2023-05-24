from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

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
