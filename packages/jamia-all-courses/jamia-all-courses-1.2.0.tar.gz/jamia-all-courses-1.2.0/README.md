# All Courses in Jamia
This repo contains index of courses available in Jamia Millia Islamia.

## Installation
```
pip install jamia-all-courses
```

## Usages
```python3
from jamia_all_courses import all_courses

for category in all_courses:
    print('-', category['name'])

    for course in category['courses']:
        print('    -', course['name'])

        for specialization in course['specializations']:
            print('        -', specialization['name'], specialization['code'])

```
Or import specific programme:
- `doctoral_programmes`
- `masters_programmes`
- `postgraduate_diploma_programmes`
- `undergraduate_programmes`
- `advanced_diploma_programmes`
- `diploma_programmes`

```python3
from jamia_all_courses import undergraduate_programmes

for course in undergraduate_programmes['courses']:
    print('    -', course['name'])
    for specialization in course['specializations']:
        print('        -', specialization['name'], specialization['code'])

```

- `getCourse(hash)`: **[category, course, specialization]**
    - Returns array of 3 with their respective labels

- `getCourseName(hash)`: Returns string of course and specialisation

```python
import get_course, get_course_name from jamia_all_courses

print(get_course_name('3fc6d'))
# B.Tech. Computer Engineering

print(get_course('3fc6d'))
# ['Undergraduate Programmes', 'B.Tech.','Computer Engineering']
```

## Structure
```
[{
    name: 'category',
    courses: [{
        name: 'course',
        specializations: [{
            name: 'specialization',
            code: 'hash'
        }]
    }]
}]
```
