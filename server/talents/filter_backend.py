from rest_framework.filters import BaseFilterBackend
from elasticsearch_dsl import Q

from talents.service import TalentService


class KeywordParserFilterBackend(BaseFilterBackend):
    """
    Custom search filter backend that interprets natural language queries.
    """

    def filter_queryset(self, request, queryset, view):
        query = request.query_params.get('q', None)
        print(query)
        if query:
            parsed_response = TalentService.process_keyword(query)


            # Initialize a list to hold all query components
            must_queries = []

            # Filter by role if it's specified
            if parsed_response.role:
                must_queries.append(Q("match", role=parsed_response.role))


            # Filter by skills if any are specified
            if parsed_response.skills:
                # Assuming 'skills' field in ES document is a list of skills
                for skill in parsed_response.skills:
                    must_queries.append(Q("match", skills=skill))

            # Filter by years of experience if specified
            if parsed_response.years_of_experience:
                # Adjust the range filter according to the years_of_experience logic
                number = parsed_response.years_of_experience[2:]
                number = int(number)
                range_query = {"gte": number} if parsed_response.years_of_experience.startswith('>=') else {"lt": number}
                must_queries.append(Q("range", years_of_experience=range_query))

            # Apply the compiled queries to the search
            if must_queries:
                queryset = queryset.query('bool', must=must_queries)

        return queryset
    
    

from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend


class CustomTalentFilterBackend(FilteringFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Get the JSON data from the request
        json_data = request.data
        query = request.query_params.get('q', None)
        print(query)
        if query:
            parsed_response = TalentService.process_keyword(query)

            # Extract role, skills, and years_of_experience from JSON
            role = parsed_response.role
            skills = parsed_response.skills
            years_of_experience = parsed_response.years_of_experience

            # Initialize a list to hold all query components
            must_queries = []

            # Filter by role if it's specified
            if role:
                must_queries.append(Q("match", role=role))

            # Filter by skills if any are specified
            if skills:
                # Assuming 'skills' field in ES document is a list of skills
                for skill in skills:
                    must_queries.append(Q("match", skills=skill))

            # Filter by years of experience if specified
            if years_of_experience:
                # Adjust the range filter according to the years_of_experience logic
                number = years_of_experience[2:]
                number = int(number)
                range_query = {"gte": number} if years_of_experience.startswith('>=') else {"lt": number}
                must_queries.append(Q("range", years_of_experience=range_query))

            # Apply the compiled queries to the search
            if must_queries:
                queryset = queryset.query('bool', must=must_queries)

        return queryset
