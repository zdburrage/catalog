#!/usr/bin/env python
# coding: utf-8

import dicttoxml
from flask import Blueprint
from flask import request
from flask import jsonify
from database import db_session
from models import Region, Recipe
from sqlalchemy import func
from inspect import getmembers
from pprint import pprint

regions = Blueprint('regions', __name__)


# Get regions
@regions.route('/regions', methods=['GET'])
def showRegions():
    count = request.args.get('count')
    catalog_mode = request.args.get('catalog')
    xml_format = request.args.get('xml')

    # Check if query parameters were added to the request
    if (catalog_mode == 'true' or catalog_mode == 'TRUE'):
        # Get the whole catalog
        region_list = db_session.query(Region).all()

        regions = []

        # Add recipes to every region
        for i in region_list:
            recipes = []
            for recipe in i.region_recipes:
                recipes.append(recipe.serialize)
            region = i.serialize
            region['recipes'] = recipes
            regions.append(region)

        serialized_result = regions

    elif (count == 'true' or count == 'TRUE'):
        # Get regions with recipe count
        region_list = db_session.query(Region).all()

        regions = []

        # Add recipes to every region
        for i in region_list:
            region = { 'name': i.name, 'id': i.id}
            region['count'] = len(i.region_recipes)
            regions.append(region)

        serialized_result = regions

    else:
        # Get all regions
        region_list = db_session.query(Region).all()
        serialized_result = [i.serialize for i in region_list]

    # Lastly we decide which data format to send
    if (xml_format == 'true' or xml_format == 'TRUE'):
        xml_output = dicttoxml.dicttoxml(serialized_result)
        return xml_output, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    else:
        return jsonify(collection=serialized_result)


@regions.route('/regions/<int:region_id>', methods=['GET'])
def showOne(region_id):
    catalog_mode = request.args.get('catalog')
    xml_format = request.args.get('xml')

    region_list = db_session.query(Region).filter(
        Region.id == region_id).all()

    # Check if query parameters were added to the request
    if (catalog_mode == 'true' or catalog_mode == 'TRUE'):
        # Get single region's catalog
        regions = []

        for i in region_list:
            recipes = []
            for recipe in i.region_recipes:
                recipes.append(recipe.serialize)
            region = i.serialize
            region['recipes'] = recipes
            regions.append(region)

        serialized_result = [regions]
    else:
        # Get single region
        serialized_result = [i.serialize for i in region_list]

    # Lastly we decide which data format to send
    if (xml_format == 'true' or xml_format == 'TRUE'):
        xml_output = dicttoxml.dicttoxml(serialized_result)
        return xml_output, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    else:
        return jsonify(collection=serialized_result)
