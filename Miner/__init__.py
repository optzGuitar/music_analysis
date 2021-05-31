from .job import Job

"""All possibly interesting positions of the note atom"""
ALL_POSITIONS = [3, 4, 5, 6]

def quantize(notelength) -> list:
    """
    This creates a list with all quantization points according to the notelength parameter.
    Parameters:
    -----------
    notelength: float
        The maximal notelength possible. Eg. 1 == Quater, 0.5 == Eights ...

    Returns:
    --------
    qunatize_points : list
        A list ocntaining all the quantize points.
    """
    counter = 0
    points = []
    while counter <= 1:
        points.append(counter)
        counter += notelength
    return points



