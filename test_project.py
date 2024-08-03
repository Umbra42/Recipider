import pytest
import project
from unittest.mock import patch

def test_Roll():
    items = ['1', '2', '3', '4', '5']
    rolled = project.Roll(items)
    assert len(rolled) == 3
    assert all(item in items for item in rolled)
    ...


def test_display(capsys: pytest.CaptureFixture[str]):
    
    project.recipider['state'] = " > displaying picked recipes"
    test_data = [{"name": "Test Recipe 1"}, {"name": "Test Recipe 2"}, {"name": "Test Recipe 3"}]
    project.display(test_data)
    captured = capsys.readouterr()
    assert "\n0: Re-Roll\n\nRecipe 1: Test Recipe 1\n\n" in captured.out
    assert "Recipe 2: Test Recipe 2\n\n" in captured.out
    assert "Recipe 3: Test Recipe 3\n\n" in captured.out

    project.recipider['state'] = " > displaying full recipe"
    test_recipe_data = {
        "ingredients": ["Test ingredient 1", "Test ingredient 2"],
        "instructions": ["Test instruction 1", "Test instruction 2"]
        }
    project.display(test_recipe_data)
    captured = capsys.readouterr()
    assert "ingredients: \n" in captured.out
    assert "Test ingredient 1" in captured.out
    assert "Test ingredient 2" in captured.out
    assert "instructions: \n" in captured.out
    assert "Test instruction 1" in captured.out
    assert "Test instruction 2" in captured.out


def test_get_user_input(monkeypatch: pytest.MonkeyPatch, capsys):
    inputs = iter(["4", "0", "1", "2", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    print(monkeypatch)
    
    options = [
        {"name": "Geroosterde aubergine en paprika met couscous, yoghurt, hummus en verse kruiden", "url": "https://recepten.lidl.nl/recept/geroosterde-aubergine-en-paprika-met-couscous-yoghurt-hummus-en-verse-kruiden", "site": "lidl"},
        {"name": "Gebakken kastanjechampignons en spinazie op een puree van aardappel en Parmezaanse kaas", "url": "https://recepten.lidl.nl/recept/gebakken-kastanjechampignons-en-spinazie-op-een-puree-van-aardappel-en-parmezaanse-kaas", "site": "lidl"},
        {"name": "Hollandse asperges uit de oven met haricots verts en een gebakken ei", "url": "https://recepten.lidl.nl/recept/hollandse-asperges-uit-de-oven-met-haricots-verts-en-een-gebakken-ei", "site": "lidl"},
    ]

    with patch('project.main', return_value=None) as mock_main, patch('sys.exit', return_value=None) as mock_exit:
        choice = project.get_user_input(options)
        captured = capsys.readouterr()
        assert "Invalid input, please try again." in captured.out
        assert "You chose to re-roll" in captured.out
        mock_main.assert_called_once()
        mock_exit.assert_called_once()

        for i, option in enumerate(options): 
            choice = project.get_user_input(options)
            captured = capsys.readouterr()  
            assert choice == option 
            assert f"You picked recipe {i + 1}: {option['name']}" in captured.out

