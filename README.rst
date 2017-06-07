==============
CountMinSketch
==============



.. image:: https://pyup.io/repos/github/gallamine/countminsketch/shield.svg
     :target: https://pyup.io/repos/github/gallamine/countminsketch/
     :alt: Updates


CountMinSketch implementation in pure python 3



Features
--------

* TODO

Example
---------


.. code:: python

    from countminsketch.countminsketch import CountMinSketch
    import numpy as np
    import matplotlib.pyplot as plt

    d = 10
    w = 100
    cms = CountMinSketch(d=10, w=100)

    a = 1.1
    s = np.random.zipf(a, 100000)

    actual_counts = {}
    for val in s:
        int_val = int(val)
        actual_counts.setdefault(int_val, 0)
        actual_counts[int_val] += 1
        cms.add(int_val)

    print("There are {} unique values in the data".format(len(actual_counts.keys())))
    print("The CountMinSketch contains {} elements".format(len(cms)))


::
    There are 43011 unique values in the data
    The CountMinSketch contains 1000 elements


.. code:: python

    est_counts = []
    for val in actual_counts.keys():
        est_counts.append(cms.query(val))

    plt.scatter(list(actual_counts.keys()), list(actual_counts.values()), color='b', label='Actual')
    plt.scatter(list(actual_counts.keys()),est_counts, color='r', label='Estimate')
    plt.legend()
    plt.yscale('log')
    plt.xlim([1,100])
    plt.xlabel('unique value')
    plt.ylabel('count of values')
    plt.title('CountMinSketch estimate vs. real for size d={}, w={}'.format(d,w))
    plt.show()


.. image:: /docs/example.png


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

