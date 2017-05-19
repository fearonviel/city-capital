#!/usr/bin/env python
import os
import jinja2
import webapp2
import random

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class City:
    def __init__(self, city, country, image):
        self.city = city
        self.country = country
        self.image = image


def city_list():
    city1 = City("Berlin", "Germany", "/assets/images/berlin.png")
    city2 = City("Ljubljana", "Slovenia", "/assets/images/ljubljana.jpg")
    city3 = City("Rome", "Italy", "/assets/images/rome.jpg")
    city4 = City("London", "Great Britain", "/assets/images/london.jpg")

    return [city1, city2, city3, city4]


class MainHandler(BaseHandler):
    def get(self):
        random_num = random.randint(0, 3)
        city = city_list()[random_num]
        params = {"city": city}

        return self.render_template("index.html", params=params)


class AnswerHandler(BaseHandler):
    def post(self):
        guess = self.request.get("guess")
        country = self.request.get("country")
        cities = city_list()

        for city in cities:
            if city.country == country:
                if city.city.lower() == guess.lower():
                    result = True
                else:
                    result = False

                params = {"result": result, "city": city}

                return self.render_template("answer.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/answer', AnswerHandler),
], debug=True)

