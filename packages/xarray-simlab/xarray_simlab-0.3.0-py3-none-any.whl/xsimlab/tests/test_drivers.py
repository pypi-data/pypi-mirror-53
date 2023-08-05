import numpy as np
import pytest
from numpy.testing import assert_array_equal
from xarray.testing import assert_identical

import xsimlab as xs
from xsimlab.drivers import (_get_dims_from_variable, BaseSimulationDriver,
                             XarraySimulationDriver)
from xsimlab.stores import InMemoryOutputStore


@pytest.fixture
def base_driver(model):
    store = {}
    out_store = InMemoryOutputStore()
    return BaseSimulationDriver(model, store, out_store)


@pytest.fixture
def xarray_driver(in_dataset, model):
    store = {}
    out_store = InMemoryOutputStore()
    return XarraySimulationDriver(in_dataset, model, store, out_store)


class TestBaseDriver:

    def test_bind_store(self, base_driver):
        base_driver.store[('init_profile', 'n_points')] = 10
        assert base_driver.model.init_profile.n_points == 10

    def test_update_store(self, base_driver):
        n = [10, 100, 1000]
        input_vars = {('init_profile', 'n_points'): n}
        base_driver.update_store(input_vars)

        assert base_driver.store[('init_profile', 'n_points')] == n
        assert base_driver.store[('init_profile', 'n_points')] is not n

    def test_update_output_store(self, base_driver):
        base_driver.store[('init_profile', 'n_points')] = 5
        base_driver.model.init_profile.initialize()

        base_driver.update_output_store([('profile', 'u')])

        expected = [np.array([1., 0., 0., 0., 0.])]
        assert_array_equal(
            base_driver.output_store[('profile', 'u')],
            expected)

    def test_run_model(self, base_driver):
        with pytest.raises(NotImplementedError):
            base_driver.run_model()


@pytest.mark.parametrize('array,clock,expected' , [
    (np.zeros((2, 2)), None, ('x', 'y')),
    (np.zeros((2, 2)), 'clock', ('x',)),
    (np.array(0), None, tuple())
])
def test_get_dims_from_variable(array, clock, expected):
    var = xs.variable(dims=[(), ('x',), ('x', 'y')])
    assert _get_dims_from_variable(array, var, clock) == expected


class TestXarraySimulationDriver:

    def test_constructor(self, in_dataset, model):
        store = {}
        out_store = InMemoryOutputStore()

        invalid_ds = in_dataset.drop('clock')
        with pytest.raises(ValueError) as excinfo:
            XarraySimulationDriver(invalid_ds, model, store, out_store)
        assert "Missing master clock" in str(excinfo.value)

        invalid_ds = in_dataset.drop('init_profile__n_points')
        with pytest.raises(KeyError) as excinfo:
            XarraySimulationDriver(invalid_ds, model, store, out_store)
        assert "Missing variables" in str(excinfo.value)

    def test_output_save_steps(self, xarray_driver):
        expected = {'clock': np.array([True, True, True, True, True]),
                    'out': np.array([True, False, True, False, True])}

        assert xarray_driver.output_save_steps.keys() == expected.keys()
        for k in expected:
            assert_array_equal(xarray_driver.output_save_steps[k], expected[k])

    @pytest.mark.parametrize('var_key,is_scalar', [
        (('init_profile', 'n_points'), True),
        (('add', 'offset'), False)
    ])
    def test_set_input_vars(self, in_dataset, xarray_driver,
                            var_key, is_scalar):
        xarray_driver._set_input_vars(in_dataset)

        actual = xarray_driver.store[var_key]
        expected = in_dataset['__'.join(var_key)].data

        if is_scalar:
            assert actual == expected
            assert np.isscalar(actual)

        else:
            assert_array_equal(actual, expected)
            assert not np.isscalar(actual)

            # test copy
            actual[0] = -9999
            assert not np.array_equal(actual, expected)

    def test_get_output_dataset(self, in_dataset, xarray_driver):
        # regression test: make sure a copy of input dataset is used
        out_ds = xarray_driver.run_model()
        assert not in_dataset.identical(out_ds)

    def test_run_model(self, in_dataset, out_dataset, xarray_driver):
        out_ds_actual = xarray_driver.run_model()

        assert out_ds_actual is not out_dataset
        assert_identical(out_ds_actual, out_dataset)

    def test_runtime_context(self, in_dataset, model):
        @xs.process
        class BadProcess:

            @xs.runtime(args='bad')
            def run_step(self, bad):
                pass

        bad_model = model.update_processes({'bad': BadProcess})

        driver = XarraySimulationDriver(in_dataset, bad_model,
                                        {}, InMemoryOutputStore())

        with pytest.raises(KeyError) as excinfo:
            driver.run_model()

        assert str(excinfo.value) == "'bad'"
