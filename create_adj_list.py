from email_graph import build_email_graph, save_adjacency_list

def main():
    """Main function to build and save the email graph."""
    print("Building email graph...")
    graph, all_emails = build_email_graph()
    
    # Save the adjacency list
    output_file = "/home/hower/studies/2025/rpg/tde1-grupos/email_graph_adjacency_list.txt"
    print(f"Saving adjacency list to {output_file}...")
    save_adjacency_list(graph, output_file)
    
    print("Done!")

if __name__ == "__main__":
    main()